# pi-hole-setup

1. Install Raspberry Pi using the [imager](https://www.raspberrypi.org/software/). Choose Raspberry PI 32 bit.
1. Before removing the memory card, run `touch ssh` in root filesystem to enable ssh.
1. Boot up pi and login `ssh pi@raspberrypi.local` (password is raspberry).
1. Install [pi-hole](https://docs.pi-hole.net/main/basic-install/)
1. Make sure the updateGravity job is disabled in `/etc/cron.d/pihole`.
1. Setup [pihole-updatelists](https://github.com/jacklul/pihole-updatelists). Update /etc/pihole-updatelist.conf per [recommended lists](https://github.com/jacklul/pihole-updatelists#recommended-lists).
2. In the pihole web interface, go to Whitelists and add the following regexes:
    - Enable Hulu: add hulu.com and hulustream.com as wildcard domains
4. Run `pihole-updatelists` to update the lists.
5. Ensure router is using pihole for DNS
    1. Reserve an IP for the pi
        1. In Google Home, go to Settings => Nest Wifi => Advanced Networking => DHCP Reservations
        1. Click the "+" and give the pi a reserved IP
    1. Set your DNS to be the PI
        1. In Google Home, go to Settings => Nest Wifi => Advanced Networking => DNS
        1. Click "Custom" and add the IP of the pi. No other nameservers should be listed


## Reference

- https://docs.pi-hole.net/main/basic-install/
- https://github.com/jacklul/pihole-updatelists
