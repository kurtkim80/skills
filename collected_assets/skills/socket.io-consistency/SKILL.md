---
name: socket.io-consistency
description: >-
  Write, review, refactor, or debug real-time Socket.IO code (io.on connection,
  socket.emit, rooms, namespaces, acknowledgements, reconnection, React clients) using
  one canonical, modern v4 idiom set. Use this skill whenever code builds chat,
  presence, live updates, or notifications over Socket.IO, or when the user hits CORS
  errors on connect, plain-WebSocket clients failing against a Socket.IO server,
  duplicate event handlers after reconnect, events missing for clients in other rooms or
  processes, memory growing with disconnected sockets, or asks rooms vs namespaces.
  Trigger it even when the user just says "push updates to connected browsers" with
  Socket.IO in the stack — without saying the words "Socket.IO idioms."
license: Complete terms in LICENSE.txt
---

# Socket.IO — consistent, modern (v4) idioms

Socket.IO is stable at v4, but generated code keeps reproducing pre-v3 patterns (implicit
CORS, version-mixed client/server), confuses it with raw WebSocket, hand-tracks sockets
in arrays where rooms exist, and re-registers handlers on every reconnect — the
duplicate-listener bug that surfaces as "every message arrives twice." This skill pins
the canonical v4 idiom set.

## Canonical idioms — always X, never Y

| Always | Never | Why |
| --- | --- | --- |
| `socket.io-client` matching the server's major version | a raw `new WebSocket(url)` against a Socket.IO server (or v2 client ↔ v4 server) | Socket.IO speaks its own protocol over Engine.IO; raw WS and cross-major clients fail with opaque connect errors. |
| explicit CORS: `new Server(httpServer, { cors: { origin: [...], credentials: true } })` | assuming same-origin or copying v2 setups with no cors block | v3+ has no implicit CORS; the symptom is failed polling requests before the upgrade. |
| rooms: `socket.join(roomId)`, `io.to(roomId).emit(...)` | hand-maintained `Map<roomId, Socket[]>` | Rooms are built in, leak-free on disconnect, and adapter-aware for multi-node. |
| know the broadcast table: `io.emit` (all), `socket.broadcast.emit` (all but sender), `io.to(r)` (room incl. sender if joined), `socket.to(r)` (room **except sender**) | guessing — especially `socket.to` vs `io.to` | The except-sender semantics of `socket.to` is the classic "why didn't I get my own message" / double-message bug. |
| acknowledgements for request-shaped exchanges: `socket.emit("save", data, (res) => ...)` / `await socket.timeout(5000).emitWithAck("save", data)` | hand-rolled reply-event correlation | Acks are built-in request/response with timeouts. |
| auth via `io.use(middleware)` + `socket.handshake.auth` | tokens in query strings | `auth` payload is the designed channel (not logged in URLs); middleware rejects before connection events fire. |
| client handler registration **once** (module/setup scope), state re-sync on `connect` | re-registering `socket.on(...)` inside reconnect/connect callbacks | Reconnection reuses the same socket object; re-adding handlers stacks duplicates. |
| per-socket state on `socket.data`, cleaned by disconnect semantics | module-level maps keyed by socket.id without disconnect cleanup | id-keyed globals grow forever; `socket.data` dies with the socket. |
| multi-node: an adapter (`@socket.io/redis-adapter`) + sticky sessions | scaling processes and hoping `io.emit` reaches everyone | Without an adapter, each node only reaches its own sockets — events silently miss half the users. |
| React: connect + register in `useEffect`, return cleanup that removes/disconnects | connecting in render / no cleanup | StrictMode double-invocation and remounts otherwise multiply connections and handlers. |

House style:

```js
// server
import { Server } from "socket.io";
const io = new Server(httpServer, {
  cors: { origin: ["https://app.example.com"], credentials: true },
});

io.use(async (socket, next) => {
  try {
    socket.data.user = await verifyToken(socket.handshake.auth.token);
    next();
  } catch {
    next(new Error("unauthorized"));
  }
});

io.on("connection", (socket) => {
  socket.on("room:join", async (roomId, ack) => {
    if (!(await canJoin(socket.data.user, roomId))) return ack({ error: "forbidden" });
    await socket.join(roomId);
    socket.to(roomId).emit("room:joined", socket.data.user.name); // others only
    ack({ ok: true });
  });

  socket.on("msg:send", (roomId, text, ack) => {
    const msg = { from: socket.data.user.name, text, at: Date.now() };
    io.to(roomId).emit("msg:new", msg);   // everyone in the room, sender included
    ack({ ok: true });
  });
});
```

## Pitfalls that produce silently wrong behavior

- **Reconnect is automatic** on the client — code that treats `disconnect` as final
  (or re-runs setup on every `connect`) drifts. Pattern: register handlers once;
  on `connect`, re-join rooms and re-sync state (the server forgot the old socket).
- **Missed-while-disconnected events are gone** — Socket.IO is not a message queue.
  Sequence/timestamp your data and fetch the gap on reconnect (or enable Connection
  State Recovery knowing its best-effort limits).
- **Rooms are server-side only**: clients can't join themselves; a "join" is always an
  event the server validates and executes. Trusting a client-sent room name without
  authorization broadcasts private data.
- **`socket.rooms` includes the socket's own id** (every socket auto-joins a room named
  by its id — that's how `io.to(socketId)` DMs work).
- **Callback-position acks**: the ack callback must be the *last* argument the emitter
  sends and the last parameter the handler accepts; misplacing it makes `ack`
  undefined — calling it then crashes the handler.
- **Binary payloads** (Buffer/ArrayBuffer/Blob) pass through natively — don't
  base64-inflate; but big files belong on HTTP, not the event channel.
- **Middleware errors** surface client-side as `connect_error` with the Error's
  message — handle that event; otherwise auth failures look like network flakiness.
- **Backpressure**: emitting large/fast streams to slow clients buffers in server
  memory (`socket.conn` buffer) — use `volatile.emit` for drop-ok data (cursors,
  tickers) and throttle the rest.

## Version notes

Target **Socket.IO 4.x** (server and client). v2↔v3+ are wire-incompatible (the
`allowEIO3: true` escape hatch exists for migration). v4.5+ added `emitWithAck` and
connection state recovery options. Python ecosystem: `python-socketio` matches by
protocol version, same idioms. Raw-WebSocket needs (binary protocols, no fallback,
non-Socket.IO peers) → use `ws`; the two don't interoperate.

## Workflow

1. Define the event contract first: names (`domain:action`), payload shapes, which
   exchanges need acks, room topology (per-document? per-user? per-tenant?).
2. Server: CORS + auth middleware → connection handler that only wires events; room
   joins validated server-side; broadcasts chosen from the table deliberately.
3. Client: one socket module (connect once, export it); handlers registered once;
   `connect`/`connect_error`/`disconnect` handled; re-sync on reconnect.
4. Plan for multiplicity from day one: `socket.data` not globals, adapter + sticky
   sessions when processes > 1, sequence numbers for gap recovery.
5. When reviewing, hunt: missing CORS config, socket arrays, `socket.to` vs `io.to`
   mixups, handlers inside connect callbacks, query-string tokens, id-keyed global
   maps, multi-node emits without an adapter.

For the broadcast matrix, namespace-vs-room decision, reconnect/state-recovery recipes,
scaling architecture, and testing patterns, read
`references/socket.io-patterns.md`.
