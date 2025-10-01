const {
    makeWASocket,
    useMultiFileAuthState,
    fetchLatestBaileysVersion,
    DisconnectReason
} = require('@whiskeysockets/baileys')

async function start() {
    const { state, saveCreds } = await useMultiFileAuthState('auth')
    const { version } = await fetchLatestBaileysVersion()

    const sock = makeWASocket({
        version,
        auth: state,
        printQRInTerminal: false
    })

    // === Pairing code dengan delay 10 detik ===
    if (!sock.authState.creds.registered) {
        const phoneNumber = '18195190839' // nomor bot
        console.log('⏳ Tunggu 10 detik untuk dapat pairing code...')
        setTimeout(async () => {
            const code = await sock.requestPairingCode(phoneNumber)
            console.log('👉 Pair this code di WhatsApp app:', code)
        }, 10000)
    }

    sock.ev.on('creds.update', saveCreds)

    sock.ev.on('connection.update', async ({ connection, lastDisconnect }) => {
        if (connection === 'open') {
            console.log('✅ Connected!')

            // === subscribe ke target biar presence update aktif ===
            for (const target of targets) {
                await sock.presenceSubscribe(target)
                console.log(`📡 Subscribed presence: ${target}`)
            }
        } else if (connection === 'close') {
            const reason = lastDisconnect?.error?.output?.statusCode
            console.log('❌ Disconnected. Reason:', reason)
            if (reason !== DisconnectReason.loggedOut) {
                console.log('🔄 Reconnecting...')
                start()
            } else {
                console.log('⚠️ Logged out. Delete folder auth/ lalu pairing ulang.')
            }
        }
    })

    // === Monitoring presence ===
    const targets = [
        '6285604739396@s.whatsapp.net',
        '6281334148237@s.whatsapp.net',
        '6281330985918@s.whatsapp.net'
    ]
    const monitorReceiver = '6281334148237@s.whatsapp.net'
    const lastStatus = {}

    sock.ev.on('presence.update', (data) => {
        for (const target of targets) {
            if (data.id === target) {
                const presence = data.presences?.[target]?.lastKnownPresence || 'offline'
                if (lastStatus[target] !== presence) {
                    lastStatus[target] = presence
                    sock.sendMessage(monitorReceiver, {
                        text: `[${new Date().toLocaleTimeString()}] ${target} is now ${presence}`
                    })
                }
            }
        }
    })

    // === Tagall feature ===
    sock.ev.on('messages.upsert', async ({ messages }) => {
        const m = messages[0]
        if (!m.message || !m.key.remoteJid) return

        const body = m.message.conversation || m.message.extendedTextMessage?.text || ''
        if (body.toLowerCase() === '.tagall') {
            try {
                const metadata = await sock.groupMetadata(m.key.remoteJid)
                const participants = metadata.participants.map(p => p.id)

                await sock.sendMessage(m.key.remoteJid, {
                    text: '👥 Tag All:\n' + participants.map(p => `@${p.split('@')[0]}`).join(' '),
                    mentions: participants
                })
            } catch (e) {
                console.error('❌ Error tagall:', e)
            }
        }
    })
}

start()
