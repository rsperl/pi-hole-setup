# pi-hole-setup

1. Install Raspberry Pi using the [imager](https://www.raspberrypi.org/software/). Choose Raspberry PI 32 bit.
1. Before removing the memory card, run `touch ssh` in root filesystem to enable ssh.
1. Boot up pi and login `ssh pi@raspberrypi.local` (password is raspberry).
1. Install [pi-hole](https://docs.pi-hole.net/main/basic-install/)
1. Make sure the updateGravity job is disabled in `/etc/cron.d/pihole`.
1. Setup [pihole-updatelists](https://github.com/jacklul/pihole-updatelists). Update /etc/pihole-updatelist.conf per [recommended lists](https://github.com/jacklul/pihole-updatelists#recommended-lists).
1. Run `pihole-updatelists` to update the lists.

