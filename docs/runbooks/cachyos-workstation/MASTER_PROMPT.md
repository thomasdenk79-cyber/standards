# CachyOS Workstation: Master-Auftrag für Codex

Version: 1.0 · 2026-09-18

## Agent-Start

Lies dieses Dokument vollständig. Erstelle `~/system-setup/` mit `INVENTORY.md`, `PLAN.md`, `CHANGES.md`, `BENCHMARKS.md`, `SECURITY.md`, `ROLLBACK.md` und `TODO.md`. Beginne mit einer lesenden Inventur. Arbeite danach phasenweise, dokumentiere Ist/Soll, überprüfe jede Änderung und setze nach einem Neustart anhand von TODO.md fort, sobald du erneut gestartet wirst. Kommunikation und Dokumentation Deutsch, Code Englisch. Keine erfundenen Erfolgsmeldungen. Nutze aktuelle offizielle Arch-/CachyOS-/Herstellerdokumentation, prüfe Paketnamen vor Installation und vermeide unbekannte AUR-Skripte.

## Sicherheits- und Freigabegrenzen

Normale Paketinstallationen und reversible Benutzer-/Desktopkonfigurationen selbstständig durchführen. Vor Änderungen an Partitionen, LUKS, Bootloader, initramfs, Secure Boot, Kernelwechsel, VFIO/GPU-Passthrough und Unternehmenssoftware explizite Zustimmung einholen. Bestehende LUKS-Verschlüsselung erhalten; kein Passwort auf Datenträger speichern. Vor SDDM-Autologin und passwortlosem sudo die Risiken erklären und separat Zustimmung einholen; auf verwalteten Geräten Unternehmensvorgaben beachten. Codex-YOLO nur als ausdrücklich gewähltes Profil (`approval_policy = "never"`, `sandbox_mode = "danger-full-access"`), nicht unbemerkt als globaler Standard; ein sicheres Standardprofil erhalten. Keine Geheimnisse, Firmendaten, Token, Konfigurationsdumps oder Gerätekennungen ins öffentliche Repository hochladen. Vor kritischen Schritten Backups, Wiederherstellungsweg und Tests festlegen. Keine globalen Sicherheitsmitigationen, Firewall oder Dienste ohne Befund deaktivieren.

## Phase 1: Inventur

Ermittle CachyOS-Version, KDE Plasma/Wayland/X11, Kernel und Scheduler (BORE vs sched-ext unterscheiden), CPU, RAM, EPP/Governor, Temperaturen/Throttling, GPUs/NVIDIA-Treiber, Secure Boot, IOMMU, Thunderbolt, SSD/NVMe, Btrfs-Subvolumes und Mount-Optionen, LUKS, Swap/zram/zswap, Audio, Bluetooth, Ethernet, WLAN, Monitor-EDID, aktive Modi, installierte Pakete und fehlerhafte Dienste. Schreibe einen konkreten Plan mit Risiken, Abhängigkeiten und Rollback.

## Phase 2: System und Performance

CachyOS vollständig über unterstützte Paketquellen aktualisieren. Passende stabile NVIDIA-Treiber samt Kernelmodulen, Vulkan/OpenGL, 32-Bit-Bibliotheken und CUDA-Kompatibilität prüfen; `nvidia-smi`, Vulkan und GPU-Auslastung testen. CachyOS-Kernel/BORE prüfen; sched-ext nicht blind parallel aktivieren. Für Netzbetrieb Gaming-/Performanceprofil und für Akku Balanced-Profil erstellen; konkurrierende Power-Manager vermeiden. I/O-Scheduler, TRIM, irqbalance, GameMode, RAM, zram/zswap, THP und relevante sysctl-Werte nur nach Bestandsaufnahme und begründeter Messung ändern. Keine Übertaktung oder thermisch kontraproduktiven Dauertakte. Vorher-/Nachher-Benchmarks mit gleichen Bedingungen dokumentieren.

## Phase 3: Btrfs

Vorhandene Btrfs-Subvolumes, `fstab`, Kompression, Snapshots und freien Speicher prüfen. Auf geeigneten Btrfs-Mounts `compress=zstd:3` konfigurieren und nach Remount/Neustart verifizieren; keine Neuformatierung, keine pauschale Rekompession. VM-Images gesondert behandeln, NOCOW nur vor dem Anlegen entsprechender Dateien erwägen. Snapper und passende Update-Snapshots/Retention sowie Btrfs-Scrub und `fstrim.timer` prüfen/einrichten; Bootloader-Integration nur nach Freigabe. Externes Backup von Snapshots unterscheiden.

## Phase 4: Monitor, Anmeldung, NVIDIA-Gaming

Samsung Odyssey Neo G9 57 Zoll: 5120×1440 bei **240 Hz** ist der bevorzugte Desktop-/Gaming-Modus; 7680×2160 bei 60 Hz nicht als automatisches Upgrade einstellen. EDID, Verbindung, Kabel, GPU-Ausgang, DSC, Farbtiefe, verfügbare Modi, reale Hz und VRR prüfen. Modus zunächst temporär mit Rückfallmöglichkeit testen, danach über KDE/KScreen dauerhaft speichern. Nur externen Monitor als primären Desktop verwenden, internes Notebookdisplay in der Sitzung deaktivieren; bei fehlendem externem Monitor muss lokaler Rückfall möglich bleiben. SDDM-Login nach gesonderter Freigabe automatisch für normalen Benutzer, niemals Root; LUKS-Passwortabfrage bleibt erhalten. Wayland bevorzugen, X11 bei belegten Problemen prüfen. KWin, VRR im Fenster-/Borderless-Modus, VSync, Frame-Pacing, MangoHud, GameMode und Gamescope spielbezogen testen; keine globalen Treiber-Hacks. Netzbetrieb bei geschlossenem Deckel nur unter Beachtung der Kühlung konfigurieren.

## Phase 5: macOS-inspiriertes KDE Plasma 6

Vorher KDE-/KScreen-/dconf-ähnliche relevante Konfiguration sichern. Elegantes Dark Theme, konsistente Qt/GTK-Optik, Fonts/Nerd Fonts, Icons, Cursor, Blur/Transparenz und Fensterdekorationen nur Plasma-6-kompatibel. Schwebendes, zentriertes Dock unten mit Autohide, schmale Topbar mit Uhr/Systemstatus, KRunner als Spotlight, Overview/virtuelle Desktops, sinnvolle Shortcuts und Dreispalten-Fensterzonen für Ultrawide. Native Plasma-Komponenten vor fragilen Widgets bevorzugen. Desktop nach Neustart testen.

## Phase 6: Terminal und Agenten

Fish als Standardshell, Starship mit kurzem Pfad, Git-Branch/-Status, Fehleranzeige ohne langen Hostnamen; Wave Terminal auf offiziell unterstütztem Weg prüfen, dazu Kitty oder passende Alternative, fastfetch, btop, fzf, ripgrep, fd, bat, eza, zoxide und tmux. Codex-Version und offizielle Installationsmethode prüfen; separates YOLO-Profil und sicheren Standard einrichten, keine unbemerkte globale Vollzugriffs-Konfiguration. Globale AGENTS.md mit Deutsch für Kommunikation, Englisch für Code, Tests, Dokumentation und kritischen Freigabepunkten. Bestehende Zugangsdaten nicht auslesen oder veröffentlichen.

## Phase 7: Netzwerk und Peripherie

Ethernet und WLAN getrennt auf Treiber/Firmware, Linkrate, Duplex, MTU, Signal, Kanalbreite, Power Save, Paketfehler, Routing, DNS und Stabilität prüfen. `ethtool`, `iw`, `iperf3` installieren, lokale Benchmarks nur mit verfügbarem Gegenpunkt; Gaming/Steam über Ethernet testen. Kein pauschaler DNS-/MTU-/Firewall-Umbau. PipeWire/WirePlumber, Bluetooth, Headset-Mikrofon, Webcam, Controller und USB/Thunderbolt prüfen.

## Phase 8: Browser, Microsoft-PWAs und Gaming

Chromium und Microsoft Edge aus vertrauenswürdigen Quellen installieren. Outlook, Teams, OneDrive und Microsoft 365 als PWAs soweit technisch unterstützt mit KDE-Startern und Benachrichtigungen einrichten; Mikrofon prüfen. OneDrive-Synchronisation und Unternehmenszugang nicht mit einer PWA gleichsetzen; keine nicht freigegebenen Drittclients. Steam, Proton/Proton-GE via ProtonUp-Qt, Wine/Winetricks, Lutris, Heroic, Vulkan 32/64 Bit, GameMode, MangoHud und optional Gamescope installieren und testen. Guild Wars 2 und ESO auf Kompatibilität prüfen, keine Account-/Anti-Cheat-Umgehung. Steam-Startoptionen spielbezogen statt global setzen.

## Phase 9: Entwicklung, Oracle/PostgreSQL und KI

Python mit uv/pipx/venv, Rust/rustup, Node/npm/TypeScript, Tauri-Abhängigkeiten, Git/GitHub CLI, VS Code, GCC/Clang/CMake, jq/yq/shellcheck installieren. VS-Code-Erweiterungen für Python, Rust, TS, SQL, PostgreSQL, Git und Remote Development. PostgreSQL-Client (`psql`, pg_dump, pg_restore, pgbench), DBeaver/pgAdmin und bei Bedarf lizenzkonform Oracle Instant Client, SQLcl/SQL Developer; psycopg 3/SQLAlchemy in Projektumgebungen. Keine produktiven Firmendatenbanken verbinden. Für lokale KI CUDA-/PyTorch-/llama.cpp-/Open-WebUI-Bedarf und GPU-VRAM prüfen, keine redundanten CUDA-Stacks.

## Phase 10: KVM und Windows-Arbeits-VM

KVM/QEMU, libvirt, virt-manager, OVMF, swtpm und VirtIO nach Hardwareprüfung vorbereiten. Windows 11 mit UEFI, TPM 2.0, Q35, geeigneter CPU/RAM-Konfiguration, QCOW2-vs-Raw-Abwägung und SPICE planen; Windows-Medium/Lizenz vom Nutzer. Btrfs-VM-Storage und COW berücksichtigen. IOMMU nur prüfen, kein VFIO/GPU-Passthrough ohne Freigabe. Firmen-Windows-VM nur bei IT-Freigabe; Smartcard, Zscaler, Ivanti, Intune, VPN und Microsoft 365 auf Kompatibilität prüfen, keine Umgehung von Unternehmensrichtlinien. Container bevorzugt Podman, Docker nur nach Bedarf.

## Abschluss

Nach jedem Abschnitt Funktionstest und Eintrag in CHANGES.md/TODO.md. Abschließend Boot/LUKS/Btrfs-Kompression/Snapshots/TRIM, NVIDIA/Vulkan, 5120×1440@240 Hz, externes Display, KDE/Autologin soweit freigegeben, Ethernet/WLAN, Audio, Steam, PWAs, Codex, Entwicklerwerkzeuge, KVM und Dienste prüfen. BENCHMARKS.md enthält Messbedingungen und echte Ergebnisse, ROLLBACK.md den Rückweg. Nicht getestete Punkte ausdrücklich als offen markieren. Beginne JETZT mit lesender Inventur, dann Plan, dann reversible Arbeiten. Stoppe an definierten Freigabegrenzen.
