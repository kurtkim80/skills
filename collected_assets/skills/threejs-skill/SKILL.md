---
name: threejs-skill
description: Build high-performance 3D web applications using Three.js (WebGL/WebGPU). Use for 3D scenes, animations, custom shaders, PBR materials, VR/XR experiences, games, data visualizations, and interactive product configurators. This is a standalone skill, not tied to Talent Architect stack.
---

# Three.js Development Skill

Three.js ile yüksek performanslı 3D web uygulamaları geliştirme rehberi.

## When to use this skill

- 3D sahne, model, animasyon veya görselleştirme geliştirirken
- WebGL/WebGPU rendering ve grafik programlamasında
- İnteraktif 3D deneyimlerde (oyun, konfiguratör, veri görsel.)
- Kamera kontrolleri, aydınlatma, materyal veya shader çalışmalarında
- 3D asset yüklemede (GLTF, FBX, OBJ) veya texture işlemede
- Post-processing efektlerde (bloom, depth of field, SSAO)
- Fizik simülasyonları veya VR/XR deneyimlerinde
- Performans optimizasyonunda (instancing, LOD, frustum culling)

---

## 1. Hızlı Başlangıç

```javascript
const scene = new THREE.Scene()
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000)
const renderer = new THREE.WebGLRenderer({ antialias: true })

renderer.setSize(window.innerWidth, window.innerHeight)
renderer.setPixelRatio(window.devicePixelRatio)
document.body.appendChild(renderer.domElement)

const geometry = new THREE.BoxGeometry()
const material = new THREE.MeshStandardMaterial({ color: 0x00ff00 })
const cube = new THREE.Mesh(geometry, material)
scene.add(cube)

const light = new THREE.DirectionalLight(0xffffff, 1)
light.position.set(5, 5, 5)
scene.add(light)
scene.add(new THREE.AmbientLight(0x404040, 0.5))

camera.position.z = 5

function animate() {
  requestAnimationFrame(animate)
  cube.rotation.x += 0.01
  cube.rotation.y += 0.01
  renderer.render(scene, camera)
}
animate()

window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight
  camera.updateProjectionMatrix()
  renderer.setSize(window.innerWidth, window.innerHeight)
})
```

---

## 2. Öğrenme Yolu

### Seviye 1 — Temel

- Sahne, kamera, renderer kurulumu
- Temel geometriler (`BoxGeometry`, `SphereGeometry`, `CylinderGeometry`)
- Standart materyaller (`MeshStandardMaterial`, `MeshBasicMaterial`)
- Render loop ve `requestAnimationFrame`

### Seviye 2 — Yaygın Görevler

- **Asset Yükleme**: `GLTFLoader`, `FBXLoader`, `OBJLoader`, `TextureLoader`
- **Texture**: UV mapping, wrapping (`RepeatWrapping`), filtering (`LinearMipMapLinearFilter`)
- **Kamera**: `PerspectiveCamera` vs `OrthographicCamera`, `OrbitControls`
- **Işık**: `DirectionalLight`, `PointLight`, `SpotLight`, `HemisphereLight`, shadow
- **Animasyon**: `AnimationMixer`, `AnimationClip`, keyframe animasyonu

### Seviye 3 — İnteraktif ve Efektler

- **Raycasting**: Mouse pick, tıklama etkileşimi
- **Post-Processing**: `EffectComposer`, bloom, SSAO, SSR
- **Transform Controls**: Drag, rotate, scale

### Seviye 4 — İleri Render

- **PBR Materyaller**: `MeshPhysicalMaterial`, roughness, metalness, normal map
- **Custom Shader**: `ShaderMaterial`, GLSL, uniform değişkenleri
- **Performans**: Instancing (`InstancedMesh`), LOD, frustum culling, `BufferGeometry`

### Seviye 5 — Uzmanlaşma

- **Fizik**: Rapier, Ammo.js entegrasyonu
- **VR/XR**: `XRSession`, `VRButton`
- **WebGPU**: `WebGPURenderer`, compute shader
- **Node Materials (TSL)**: Shader graph

---

## 3. Temel Kavramlar

### Sahne Grafiği

```javascript
const scene = new THREE.Scene() // Kök node
const group = new THREE.Group() // Gruplayıcı
const mesh = new THREE.Mesh(geo, mat) // Görünür obje
const light = new THREE.PointLight() // Işık kaynağı

group.add(mesh)
scene.add(group, light)
```

### Geometri ve BufferGeometry

```javascript
const boxGeo = new THREE.BoxGeometry(1, 1, 1)
const sphereGeo = new THREE.SphereGeometry(0.5, 32, 32)
const torusGeo = new THREE.TorusGeometry(0.5, 0.2, 16, 100)

const custom = new THREE.BufferGeometry()
const vertices = new Float32Array([0, 0, 0, 1, 0, 0, 0, 1, 0])
custom.setAttribute('position', new THREE.BufferAttribute(vertices, 3))
```

### PBR Materyal

```javascript
const material = new THREE.MeshStandardMaterial({
  color: 0xffffff,
  roughness: 0.5,
  metalness: 0.2,
  map: colorTexture,
  normalMap: normalTexture,
  roughnessMap: roughnessTexture,
  envMap: envMapTexture,
  envMapIntensity: 1.0,
})
```

### Texture Yükleme

```javascript
const loader = new THREE.TextureLoader()
const texture = loader.load('/textures/color.jpg', (tex) => {
  tex.wrapS = THREE.RepeatWrapping
  tex.wrapT = THREE.RepeatWrapping
  tex.repeat.set(4, 4)
})

const gltfLoader = new GLTFLoader()
gltfLoader.load('/models/model.gltf', (gltf) => {
  scene.add(gltf.scene)
})
```

---

## 4. Performans

### Instancing (Çok Sayıda Aynı Obje)

```javascript
const count = 1000
const geometry = new THREE.BoxGeometry(0.1, 0.1, 0.1)
const material = new THREE.MeshStandardMaterial()
const mesh = new THREE.InstancedMesh(geometry, material, count)

const matrix = new THREE.Matrix4()
for (let i = 0; i < count; i++) {
  matrix.setPosition(Math.random() * 10, Math.random() * 10, Math.random() * 10)
  mesh.setMatrixAt(i, matrix)
}
mesh.instanceMatrix.needsUpdate = true
scene.add(mesh)
```

### LOD (Level of Detail)

```javascript
const lod = new THREE.LOD()
lod.addLevel(highDetailMesh, 0)
lod.addLevel(mediumDetailMesh, 50)
lod.addLevel(lowDetailMesh, 200)
scene.add(lod)
```

### Genel Kurallar

- `renderer.info` ile draw call'ları takip et
- Texture atlas kullan — HTTP request sayısını azaltır
- Geometry'yi `dispose()` ile bellekten temizle
- Aynı materyal/geometry'yi yeniden kullan
- `frustumCulled = true` (varsayılan) — ekran dışı nesneleri atla

---

## 5. Raycasting (Mouse Etkileşimi)

```javascript
const raycaster = new THREE.Raycaster()
const mouse = new THREE.Vector2()

window.addEventListener('mousemove', (e) => {
  mouse.x = (e.clientX / window.innerWidth) * 2 - 1
  mouse.y = -(e.clientY / window.innerHeight) * 2 + 1
})

function checkIntersections() {
  raycaster.setFromCamera(mouse, camera)
  const intersects = raycaster.intersectObjects(scene.children, true)

  if (intersects.length > 0) {
    const hit = intersects[0].object
    console.log('Tıklanan:', hit.name, 'Nokta:', intersects[0].point)
  }
}
```

---

## 6. Custom Shader

```javascript
const material = new THREE.ShaderMaterial({
  uniforms: {
    uTime: { value: 0 },
    uColor: { value: new THREE.Color(0x00ff00) },
  },
  vertexShader: `
    uniform float uTime;
    varying vec2 vUv;
    void main() {
      vUv = uv;
      vec3 pos = position;
      pos.y += sin(pos.x * 5.0 + uTime) * 0.1;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
    }
  `,
  fragmentShader: `
    uniform vec3 uColor;
    varying vec2 vUv;
    void main() {
      gl_FragColor = vec4(uColor * vUv.x, 1.0);
    }
  `,
})

function animate() {
  requestAnimationFrame(animate)
  material.uniforms.uTime.value += 0.01
  renderer.render(scene, camera)
}
```

---

## 7. Animasyon (GLTF Modeli)

```javascript
let mixer: THREE.AnimationMixer

gltfLoader.load('/model.gltf', (gltf) => {
  scene.add(gltf.scene)
  mixer = new THREE.AnimationMixer(gltf.scene)

  const action = mixer.clipAction(gltf.animations[0])
  action.play()
})

const clock = new THREE.Clock()
function animate() {
  requestAnimationFrame(animate)
  const delta = clock.getDelta()
  mixer?.update(delta)
  renderer.render(scene, camera)
}
```

---

## 8. Kaynaklar

- Resmi Dokümantasyon: https://threejs.org/docs/
- Örnekler: https://threejs.org/examples/
- Editor: https://threejs.org/editor/
- Discord: https://discord.gg/56GBJwAnUS
- Three.js Journey (kurs): https://threejs-journey.com/

---

## 6. GLSL Shaders Referansı

### ShaderMaterial vs RawShaderMaterial

```javascript
// ShaderMaterial — Three.js built-in uniforms/attributes otomatik gelir
// (modelMatrix, modelViewMatrix, projectionMatrix, position, normal, uv)
const material = new THREE.ShaderMaterial({
  uniforms: { time: { value: 0 } },
  vertexShader: `
    void main() {
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
  fragmentShader: `
    uniform float time;
    void main() { gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0); }
  `,
})

// RawShaderMaterial — her şeyi kendin tanımla
const material = new THREE.RawShaderMaterial({
  vertexShader: `
    precision highp float;
    attribute vec3 position;
    uniform mat4 projectionMatrix;
    uniform mat4 modelViewMatrix;
    void main() {
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
})
```

### Uniform Tipleri

```javascript
uniforms: {
  floatVal:    { value: 1.5 },
  vec2Val:     { value: new THREE.Vector2(1, 2) },
  vec3Val:     { value: new THREE.Vector3(1, 2, 3) },
  colorVal:    { value: new THREE.Color(0xff0000) },  // → vec3 olarak
  mat4Val:     { value: new THREE.Matrix4() },
  textureVal:  { value: texture },                    // → sampler2D
  floatArray:  { value: [1.0, 2.0, 3.0] },
}

// Animation loop'ta güncelleme
material.uniforms.time.value = clock.getElapsedTime()
material.uniforms.color.value.setHSL(hue, 1, 0.5)
```

### Varying'ler (Vertex → Fragment)

```glsl
// Vertex shader
varying vec2 vUv;
varying vec3 vNormal;

void main() {
  vUv = uv;
  vNormal = normalize(normalMatrix * normal);
  gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
}

// Fragment shader
varying vec2 vUv;
varying vec3 vNormal;

void main() {
  gl_FragColor = vec4(vNormal * 0.5 + 0.5, 1.0);
}
```

### Yaygın Shader Efektleri

```glsl
// Vertex displacement (dalga)
uniform float time;
uniform float amplitude;
void main() {
  vec3 pos = position;
  pos.z += sin(pos.x * 5.0 + time) * amplitude;
  pos.z += sin(pos.y * 5.0 + time) * amplitude;
  gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
}

// Fresnel efekti
varying vec3 vNormal;
varying vec3 vWorldPosition;
void main() {
  vec3 viewDir = normalize(cameraPosition - vWorldPosition);
  float fresnel = pow(1.0 - dot(viewDir, vNormal), 3.0);
  gl_FragColor = vec4(mix(vec3(0.0,0.0,0.5), vec3(0.5,0.8,1.0), fresnel), 1.0);
}

// Dissolve efekti
uniform float progress;
uniform sampler2D noiseMap;
void main() {
  float noise = texture2D(noiseMap, vUv).r;
  if (noise < progress) discard;
  float edge = smoothstep(progress, progress + 0.1, noise);
  gl_FragColor = vec4(mix(vec3(1.0,0.5,0.0), vec3(0.5), edge), 1.0);
}

// Value noise
float random(vec2 st) {
  return fract(sin(dot(st.xy, vec2(12.9898,78.233))) * 43758.5453);
}
float noise(vec2 st) {
  vec2 i = floor(st);
  vec2 f = fract(st);
  float a = random(i), b = random(i + vec2(1,0));
  float c = random(i + vec2(0,1)), d = random(i + vec2(1,1));
  vec2 u = f * f * (3.0 - 2.0 * f);
  return mix(a,b,u.x) + (c-a)*u.y*(1.0-u.x) + (d-b)*u.x*u.y;
}
```

### Built-in Shader'ı Extend Etme (onBeforeCompile)

```javascript
const material = new THREE.MeshStandardMaterial({ color: 0x00ff00 })

material.onBeforeCompile = (shader) => {
  shader.uniforms.time = { value: 0 }
  material.userData.shader = shader

  shader.vertexShader = 'uniform float time;\n' + shader.vertexShader
  shader.vertexShader = shader.vertexShader.replace(
    '#include <begin_vertex>',
    `
    #include <begin_vertex>
    transformed.y += sin(position.x * 10.0 + time) * 0.1;
    `,
  )
}

// Animation loop'ta güncelle
if (material.userData.shader) {
  material.userData.shader.uniforms.time.value = clock.getElapsedTime()
}
```

### GLSL Yerleşik Fonksiyonlar

```glsl
// Math
abs, sign, floor, ceil, fract, mod, min, max
clamp(x, min, max), mix(a, b, t), step(edge, x), smoothstep(edge0, edge1, x)
pow, exp, log, sqrt, inversesqrt

// Trigonometri
sin, cos, tan, asin, acos, atan(y,x)
radians(deg), degrees(rad)

// Vektör
length(v), distance(p0, p1), dot(x, y), cross(x, y), normalize(v)
reflect(I, N), refract(I, N, eta)

// Texture
texture2D(sampler, coord)           // GLSL 1.0
texture(sampler, coord)             // GLSL 3.0 (glslVersion: THREE.GLSL3)
textureCube(sampler, coord)
```

### Material Özellikleri

```javascript
new THREE.ShaderMaterial({
  transparent: true,
  side: THREE.DoubleSide,
  depthTest: true,
  depthWrite: false,
  blending: THREE.AdditiveBlending, // NormalBlending, SubtractiveBlending
  wireframe: false,
  glslVersion: THREE.GLSL3,
  extensions: {
    derivatives: true, // fwidth, dFdx, dFdy için
    fragDepth: true, // gl_FragDepth için
  },
})
```

### Instanced Shader

```javascript
const offsets = new Float32Array(instanceCount * 3)
geometry.setAttribute('offset', new THREE.InstancedBufferAttribute(offsets, 3))

// Vertex shader'da
// attribute vec3 offset;
// vec3 pos = position + offset;
```

### Hata Ayıklama

```javascript
renderer.debug.checkShaderErrors = true

// Fragment shader'da görsel debug
gl_FragColor = vec4(vUv, 0.0, 1.0) // UV göster
gl_FragColor = vec4(vNormal * 0.5 + 0.5, 1.0) // Normal göster
```

### Performans İpuçları

```glsl
// ❌ Conditional (GPU'da yavaş)
if (value > 0.5) { color = colorA; } else { color = colorB; }

// ✅ step/mix ile branchless
color = mix(colorB, colorA, step(0.5, value));
```
