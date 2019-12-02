module.exports = {
  parser: '@typescript-eslint/parser',
  env: {
    node: true,
  },
  extends: [
    'eslint:recommended',
    'prettier',
    'prettier/@typescript-eslint',
    'plugin:@typescript-eslint/eslint-recommended',
    'plugin:@typescript-eslint/recommended',
  ],
  globals: {
    Atomics: 'readonly',
    SharedArrayBuffer: 'readonly',
  },
  parserOptions: {
    project: './tsconfig.json',
    ecmaVersion: 2018,
    sourceType: 'module',
  },
  plugins: ['@typescript-eslint'],
  rules: {
    '@typescript-eslint/indent': 0,
    '@typescript-eslint/interface-name-prefix': 0,
    '@typescript-eslint/array-type': 0,
    '@typescript-eslint/camelcase': 1,
  },
};
