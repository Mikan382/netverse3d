import * as THREE from 'three';
import { BokehPass } from 'three/addons/postprocessing/BokehPass.js';
import { ShaderPass } from 'three/addons/postprocessing/ShaderPass.js';
import { ALLEY_LAMP_LIGHT_OFFSET } from '../../runtime/alley-showcase.mjs';

export function createAlleyRoadMaterial(surface, model, wetness) {
  const road = surface.clone();
  road.uniforms = { ...surface.uniforms, wetness: { value: wetness } };
  const sources = road.uniforms.reflectionSources.value;
  const position = new THREE.Vector3();
  const orientation = new THREE.Quaternion();
  const head = new THREE.Vector3();
  let count = 0;
  model.traverse((node) => {
    const lamp = /^lamp_a_\d+$/.test(node.name);
    if ((!lamp && !/^sign_[ab]_\d+$/.test(node.name)) || count >= sources.length) return;
    node.getWorldPosition(position);
    if (lamp) {
      node.getWorldQuaternion(orientation);
      position.add(head.fromArray(ALLEY_LAMP_LIGHT_OFFSET).applyQuaternion(orientation));
    }
    sources[count++].set(position.x, position.y, position.z, Number(lamp));
  });
  return road;
}

export function createAlleyCameraEffects(scene, camera, composer) {
  const focus = new BokehPass(scene, camera, { focus: 3, aperture: 0.005, maxblur: 0.009 });
  const blur = new ShaderPass({
    uniforms: { tDiffuse: { value: null }, velocity: { value: new THREE.Vector2() } },
    vertexShader: `
      varying vec2 vUv;
      void main() {
        vUv = uv;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }
    `,
    fragmentShader: `
      uniform sampler2D tDiffuse;
      uniform vec2 velocity;
      varying vec2 vUv;
      void main() {
        vec4 color = vec4(0.0);
        for (int i = 0; i < 5; i++) {
          vec2 uv = clamp(vUv + velocity * (float(i) / 4.0 - 0.5), 0.0, 1.0);
          color += texture2D(tDiffuse, uv);
        }
        gl_FragColor = color * 0.2;
      }
    `,
  });
  focus.enabled = false;
  blur.enabled = false;
  composer.addPass(focus);
  composer.addPass(blur);
  const target = new THREE.Vector3();
  const velocity = blur.uniforms.velocity.value;

  return {
    setActive(active) {
      focus.enabled = active;
      blur.enabled = active;
      velocity.set(0, 0);
    },
    sample(shot, continuous) {
      target.fromArray(shot.target);
      focus.uniforms.focus.value = Math.hypot(
        target.x - shot.position[0],
        target.y - shot.position[1],
        target.z - shot.position[2],
      );
      velocity.set(0, 0);
      if (continuous) {
        target.fromArray(shot.target).project(camera);
        velocity.set(target.x, target.y).multiplyScalar(0.34).clampLength(0, 0.016);
      }
    },
  };
}
