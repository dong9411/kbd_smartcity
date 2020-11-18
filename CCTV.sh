sudo ip route add 169.254.0.0/16 dev enp0s31f6
# To-do: Use nmap to dynamically add CCTV
# To-do: Dockerize!
socat TCP4-LISTEN:8554,fork,reuseaddr TCP4:169.254.232.7:554
socat UDP4-LISTEN:8554,fork,reuseaddr UDP4:169.254.232.7:554