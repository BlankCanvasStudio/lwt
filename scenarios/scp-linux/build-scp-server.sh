#!/bin/bash

sudo apt-get update && sudo apt-get upgrade

sudo apt install -y git

cd ~

git clone https://github.com/torvalds/linux.git

cat <<EOF > id_rsa
-----BEGIN OPENSSH PRIVATE KEY-----
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
PAV+JyQJHPZkcAAAAJYWRhbUBlZGVuAQI=
-----END OPENSSH PRIVATE KEY-----
EOF


cat <<EOF > id_rsa.pub
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDI604XPYWRxwBnX1K+PpIENrPNjEPKSgTItfaiB6iXXSiofjp2Yeq/zqTPlDIVvpSbnCvOohu8G1OOQf9vIJCfWZ2WKj+g42I35vDPNjxXVNZgpevyGKZpEmHNFv+yTVSWSkZm+/qP+1YKTvtPGUZDTg1eDuJXWGFYxD0Ybv/e0b6ucMqItG3JY0QZHGjznikyFqhCMRHZmRuZ1iJm76dLd3ah7DEnm1HfiuytsUd+tIgvWGDN95ZJEp5H3EIX5i08oAyl3WNHUVJLQrPnvfcMFN5ALnsJSyX5N2ef/nH17aVWN4URsRd3fFct3iY2F2qLWtE+jWQj3yhBp98jpAZ8wGiLAsIBguP2Ues+xnsem7D4h1/AK4/k+EpQ4H1xyRd9kXQmQwrWwlqw2cTWDy+OrwdxEANhjL7AtbgstTQ7uBZcyiCf05+9iBIQfMfJ/X34qXL2LOq7IFDKHaHv4gw8GVgcnSCrXQhRQPub92OgcCozTBbBOnTgRmJg5xLuyBs=
EOF


# Allow tap user to ssh into tap server
cat <<EOF > /home/blankcanvas/.ssh/authorized_keys
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDI604XPYWRxwBnX1K+PpIENrPNjEPKSgTItfaiB6iXXSiofjp2Yeq/zqTPlDIVvpSbnCvOohu8G1OOQf9vIJCfWZ2WKj+g42I35vDPNjxXVNZgpevyGKZpEmHNFv+yTVSWSkZm+/qP+1YKTvtPGUZDTg1eDuJXWGFYxD0Ybv/e0b6ucMqItG3JY0QZHGjznikyFqhCMRHZmRuZ1iJm76dLd3ah7DEnm1HfiuytsUd+tIgvWGDN95ZJEp5H3EIX5i08oAyl3WNHUVJLQrPnvfcMFN5ALnsJSyX5N2ef/nH17aVWN4URsRd3fFct3iY2F2qLWtE+jWQj3yhBp98jpAZ8wGiLAsIBguP2Ues+xnsem7D4h1/AK4/k+EpQ4H1xyRd9kXQmQwrWwlqw2cTWDy+OrwdxEANhjL7AtbgstTQ7uBZcyiCf05+9iBIQfMfJ/X34qXL2LOq7IFDKHaHv4gw8GVgcnSCrXQhRQPub92OgcCozTBbBOnTgRmJg5xLuyBs=
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDFzl6zZwssVjyoMpxvG2DCeHq/ZbLQFH3OiO1qxoelwVkq6LikIthVa5jKgNwBbGN7m+UJ1JBhD4w5buYeSFPYR9IR+ccjXYtPSAsFBKaWnZUo6JpW2MzMv4gdKYFIWwJ6ijwJL2K/MFwMo/+u6RKpTVQ/zFqMfDybLd+Q+EQjh/YZyZ84HRBkJNropRMyjw+5Ar2876e5NGyyOnlrQcprTZhe124W6V3JkIpkeeISwmIjuOD8vpBhWoCexjRKxTS5Y7q6n+SPGmVvD+4aElO/Tt7sy6S3E5rzyX9q9wAMefVZoS1i63QqY5vsW1uYREPAPhX3njbiDbKa6a1Ez9EQf6Nk1BjCPhDnHCq7MLIgILO60sZ+xI8Oco6VFfVSbiEEknMZbOzDSPIu8V7uNYEf1Zx0o+NLEoP7TBxKWMkaEGLa/q3tmuiJw2Xp4qLJFrMsq/7co8Zzvos3H0P1rxUGllReM3TldajjiFeW/3VgtXrO4IijAEdh83U8LSJro+mY2iFKjhWYlLG08kLmA8kmVCwVG9EBh119IaXEdXJND1vdobcVOkQNJrq0iZHR36g8sswR1xLIt8+3xzEDQmdBUxi2oma4CF8+u/mLxZetXojsOhT2uswm61hrI6lpXBODEF6T9oEHbli3iZnLCFEo7iO5HEKh8fG6Ihp38FqoMw==
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDa28b1sSRT1PiPioIeTCwZzK6xjeLWeavzcV2/6J6FFClb91Mdgt01GGEfvNWKVOYPGM4zof/YIGKyEjCDJjfRFVdbHuQf5b85bE2uHNIJ/MvC/2i89lHSHNh/hh73D+1XiTUxoRM8kZ3ZI1lS4OByLzSNuS8ehqPbJSVx++m9BRcF51dmeJjYQdzWL/j8ZJ021FIicKH9zEznigb6KCwLgyaHND+Zv/RZE6fnHcOJZU8TItXfKIGX9qFiPhEHzanfFP9+Emp50dlNg0zL2zoxIOnhQ4UkY7eLSJDTCUdjZVA76wJMUY572P/4F0OTaNn4o1lQ8Feyjcdd8zxZ460UFTfmakqtVK21kURMHn8dV7x343CnKc+cOKaGANFyMikabpahJ6uOKZfwrFwjQQ5Ni61xrdDSjV5gNLnM61b8wbG254f0qPeBm0q4v32ZWisQp5mzXidTv63brpXcKm8w7iTla94O8dA2I/gn+MQ1R6jFmoIH0P2XrqKRwBXRzzs=
EOF

 
