# ntnx-escape-game
Roleplay to discover Nutanix platform

# Preparation
- Book a HPOC with Nutanix Self-Service activated
    - Multinode-cluster
    - AOS 7 <- May need manual update
    - PC2024.3 <- May need manual update
    - NSS enabled
    - Leap Enabled
    - Flow security enabled
    - Files with old version 
- Upload the runbook  `blueprint/EG-prerequisites.json` in the `lab` project
- Launch it
- Upload the blueprint `blueprint/EG-EscapeGame.json` in the `lab` project
- Update NUTANIX credential with password `nutanix/4u`
- Select cluster and primary Network
- Launch it

# Player prerequisites
- Players need to have VPN access to HPOC (is going to be updated and use VDI for a more convenient approach)

# Game launch
- Use Day 2 action of the BP to :
  - Start web services
  - Launch invitation email to your players (you'll have to enter recipients list)
  - Launch "End of lab" email (1st recipients list will be used)

Self Service Application description will provide URL to play, as it will mentioned in the invitation email too.

