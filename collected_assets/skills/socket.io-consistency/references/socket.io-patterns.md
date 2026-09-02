# Socket.IO patterns — deep reference

Target: Socket.IO 4.x (Node server, JS client; python-socketio follows the same
protocol). Read this when a SKILL.md rule needs justification or delivery semantics
matter.

## 1. The broadcast matrix

| Call | Reaches |
| --- | --- |
| `io.emit("e")` | every connected socket (default namespace) |
| `socket.emit("e")` | that one socket |
| `socket.broadcast.emit("e")` | everyone **except** the sender |
| `io.to("room").emit("e")` | every socket in the room (sender too, if joined) |
| `socket.to("room").emit("e")` | room members **except** the sender |
| `io.to("r1").to("r2").emit("e")` | union of rooms (deduped) |
| `io.except("room").emit("e")` | everyone not in the room |
| `io.to(socketId).emit("e")` | one socket (id auto-room) |
| `io.of("/admin").emit("e")` | a namespace's sockets |
| `socket.volatile.emit("e")` | best-effort; dropped if the client isn't ready |
| `io.local.emit("e")` | this node only (skip the adapter) |

Chat-message rule of thumb: sender renders optimistically → `socket.to(room)`;
sender waits for the server echo → `io.to(room)`. Pick one per event type and write it
down in the contract.

## 2. Rooms vs namespaces

| | Rooms | Namespaces |
| --- | --- | --- |
| granularity | dynamic, per-socket join/leave | static-ish, separate connection contexts |
| middleware/auth | shared with namespace | own `use()`, own handlers |
| client awareness | invisible to client | client connects to `io("/admin")` explicitly |
| use for | documents, chats, tenants, per-user channels | genuinely different protocols/auth domains (admin vs app) |

Default to **one namespace, many rooms**. Multiplexing note: namespaces share one
underlying connection — they're cheap; they're just rarely *necessary*.

Canonical room shapes: `user:{id}` (joined by all of a user's tabs/devices — DM
delivery is `io.to(`user:${id}`)`), `doc:{id}`, `tenant:{id}`.

## 3. Acknowledgements

```js
// Client request/response with timeout (v4.5+)
try {
  const res = await socket.timeout(5000).emitWithAck("doc:save", payload);
} catch (e) {
  // no ack within 5s — server down, handler missing, or ack never called
}

// Callback style (both directions work the same)
socket.emit("doc:save", payload, (res) => { ... });

// Server handler — ack is the LAST parameter
socket.on("doc:save", async (payload, ack) => {
  try {
    await save(payload);
    ack({ ok: true });
  } catch (err) {
    ack({ ok: false, error: "save_failed" });
  }
});
```

- Every code path in an acked handler must call `ack` exactly once — a thrown
  exception that skips it leaves the client timing out.
- Server→client acks: `socket.timeout(5000).emit("e", data, (err, res) => ...)` —
  note the err-first signature with timeout on the server side.
- Broadcasts can't be acked (v4.6 added `io.timeout().emit` aggregate acks —
  specialized; don't design around it).

## 4. Lifecycle and reconnection

### Client module (the one-socket pattern)

```js
// socket.js
import { io } from "socket.io-client";

export const socket = io("https://api.example.com", {
  auth: { token: () => localStorage.getItem("token") }, // function form: fresh on reconnect
  // autoConnect: false if you must wait for login; then socket.connect() after
});

socket.on("connect", () => {
  // the server forgot us: re-join rooms / request missed data
  socket.emit("session:resume", { since: lastSeq });
});
socket.on("connect_error", (err) => {
  if (err.message === "unauthorized") redirectToLogin();
});
socket.on("disconnect", (reason) => {
  // "io server disconnect" → server called socket.disconnect(); manual reconnect needed
  // others → auto-reconnect will handle it
});
```

### React

```jsx
useEffect(() => {
  const onMsg = (m) => setMessages((prev) => [...prev, m]);
  socket.on("msg:new", onMsg);
  return () => socket.off("msg:new", onMsg);   // exact-handler off — not socket.off()
}, []);
```

- Removing with the same function reference is what makes cleanup correct;
  anonymous inline handlers can't be removed individually.
- Connection state in UI: track via `connect`/`disconnect` events into state, render
  a degraded banner — don't gate every emit on guesses.

### Missed events

Disconnected clients receive nothing retroactively. Two sane designs:

1. **Sequence + backfill**: server stamps events (`seq`); client stores the last seen;
   on `connect`, fetch `since=seq` over the same socket or HTTP.
2. **Connection State Recovery** (v4.6+): `new Server(srv, { connectionStateRecovery:
   {} })` restores rooms and replays missed packets within `maxDisconnectionDuration`
   — *best effort* (check `socket.recovered`); still implement backfill for the
   non-recovered path.

## 5. Server-side state and cleanup

```js
io.on("connection", (socket) => {
  socket.data.user = socket.data.user;            // set by auth middleware
  socket.data.openedAt = Date.now();

  socket.on("disconnect", async (reason) => {
    // rooms are auto-left; do app-level presence here
    const stillOnline = (await io.in(`user:${socket.data.user.id}`).fetchSockets()).length > 0;
    if (!stillOnline) publishPresence(socket.data.user.id, "offline");
  });
});
```

- `socket.data` is the per-connection store (and is shared through `fetchSockets()`
  across nodes with an adapter).
- Presence must account for multi-tab: a user is offline when their *room* empties,
  not when one socket closes.
- Introspection: `io.in(room).fetchSockets()`, `io.sockets.adapter.rooms` (local view
  only without adapter awareness).

## 6. Scaling beyond one process

```js
import { createAdapter } from "@socket.io/redis-adapter";
const pub = createClient({ url: REDIS_URL });
const sub = pub.duplicate();
await Promise.all([pub.connect(), sub.connect()]);
io.adapter(createAdapter(pub, sub));
```

Two independent requirements:

1. **Adapter** (redis/postgres/cluster): routes `io.emit`/room broadcasts across nodes.
   Without it, emits reach only the local node's sockets — partial delivery with no
   errors.
2. **Sticky sessions** at the load balancer: the HTTP long-polling handshake spans
   multiple requests that must hit one node (cookie-based LB stickiness, or
   `transports: ["websocket"]` client-side to skip polling — at the cost of fallback).

Emitting from outside the socket server (workers, cron) — `@socket.io/redis-emitter`
publishes through the same adapter instead of importing `io` everywhere.

## 7. Event contract hygiene

- Names: `domain:action` (`msg:new`, `doc:update`, `presence:change`); payloads are
  single objects (extensible) except where acks need tuples.
- Validate inbound payloads server-side (zod/ajv) — sockets are as untrusted as HTTP
  bodies.
- Reserved names you must not emit: `connect`, `disconnect`, `connect_error`,
  `newListener`/`removeListener` (EventEmitter inheritance).
- TypeScript: type the maps once, share between client and server:

  ```ts
  interface ServerToClientEvents { "msg:new": (m: Msg) => void }
  interface ClientToServerEvents { "msg:send": (roomId: string, text: string, ack: (r: Ack) => void) => void }
  const io = new Server<ClientToServerEvents, ServerToClientEvents>(srv);
  ```

## 8. Testing

```js
// Integration: real server on an ephemeral port + real client
let io, clientSocket;
beforeAll((done) => {
  const httpServer = createServer();
  io = new Server(httpServer);
  httpServer.listen(() => {
    const port = httpServer.address().port;
    clientSocket = ioc(`http://localhost:${port}`);
    io.on("connection", registerHandlers);
    clientSocket.on("connect", done);
  });
});
afterAll(() => { io.close(); clientSocket.disconnect(); });

test("echoes to room", (done) => {
  clientSocket.emit("room:join", "r1", () => {
    clientSocket.on("msg:new", (m) => { expect(m.text).toBe("hi"); done(); });
    clientSocket.emit("msg:send", "r1", "hi", () => {});
  });
});
```

Real-socket integration tests beat mocking the io object — the semantics under test
*are* the delivery semantics. Keep them on ephemeral ports, close everything in
teardown (open handles hang Jest).

## 9. Review checklist

1. No/implicit CORS; client and server majors mismatched; raw WebSocket clients.
2. Socket arrays/maps instead of rooms; id-keyed globals without disconnect cleanup.
3. `socket.to` vs `io.to` vs `broadcast` chosen by vibes; sender-echo bugs.
4. Handlers registered inside `connect` callbacks; React effects without cleanup.
5. Tokens in query strings; unvalidated inbound payloads; client-chosen rooms
   unauthorized.
6. No reconnect re-sync; reliance on Socket.IO as a message queue.
7. Multi-process deployments without adapter + sticky sessions.
8. Acked handlers with paths that never call ack; large blobs over events.
