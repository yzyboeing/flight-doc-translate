'use strict';

const { createStyleSet } = require('./_style_factory.js');

let configured = null;

function configure(palette) {
  if (!palette || !palette.primary) {
    throw new Error('Sample the source PDF first, then provide palette.primary');
  }
  configured = createStyleSet({
    color: true,
    primary: palette.primary,
    secondary: palette.secondary || palette.primary,
  });
  return configured;
}

function active() {
  if (!configured) {
    throw new Error('style_boeing.configure({ primary, secondary }) must be called with colors sampled from the source PDF');
  }
  return configured;
}

const api = { configure };
for (const name of ['p', 'b1', 'b2', 'h2', 'h3', 'note', 'cell', 'figure', 'figCap', 'keyTable', 'gap', 'rule', 'run']) {
  api[name] = (...args) => active()[name](...args);
}
Object.defineProperty(api, 'palette', { enumerable: true, get: () => active().palette });

module.exports = api;
