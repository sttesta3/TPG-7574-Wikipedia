import time
import random
import subprocess


def caos(servicios: list):
    
    randomSleep = random.randint(5,15)
    time.sleep(float(randomSleep))

    while True:
        randomProba = random.randint(1,3)

        if randomProba == 1: # 1/3 de que pueda matar un servicio   
            servicio = random.randint(0, len(servicios)-1)

            if "cliente" in servicios[servicio].lower():
                continue

            subprocess.run(["sudo", "docker", "stop", servicios[servicio]])
            print(f"[INFO] Mato al servicio {servicios[servicio]}") 
            


def main():
    
    dockerPs = subprocess.run(["sudo", "docker", "ps", "-a"], capture_output=True, text=True)

    dockerPsSplit = dockerPs.stdout.split("\n")
    dockerPsSplit.pop(0)

    servicios = []
    for v in dockerPsSplit:
        if v == "":
            continue
        
        servicios.append(list(filter(lambda x: x != "", v.split(" ")))[-1])

    caos(servicios)

if __name__ == "__main__":
    main()