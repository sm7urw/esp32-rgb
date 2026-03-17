import urequests
import hashlib

def check_for_updates():
    """Kollar om det finns en nyare version på GitHub"""
    try:
        # Hämta versionsnummer från GitHub
        version_url = "https://raw.githubusercontent.com/sm7urw/esp32-rgb/main/version.txt"
        remote_version = urequests.get(version_url).text.strip()
        
        # Läs lokal version
        try:
            with open("version.txt", "r") as f:
                local_version = f.read().strip()
        except:
            local_version = "0"
        
        if remote_version != local_version:
            print(f"Uppdatering tillgänglig: {local_version} -> {remote_version}")
            
            # Hämta ny RGB-kontroll
            code_url = "https://raw.githubusercontent.com/dittAnvändarnamn/esp32-rgb/main/rgb_control.py"
            response = urequests.get(code_url)
            
            # Spara lokalt
            with open("rgb_control.py", "w") as f:
                f.write(response.text)
            
            # Spara version
            with open("version.txt", "w") as f:
                f.write(remote_version)
            
            print("Firmware uppdaterad!")
            return True
        else:
            print("Redan uppdaterad")
            return False
            
    except Exception as e:
        print("Uppdateringscheck misslyckades:", e)
        return False

# main.py
connect_wifi()

# Kollar för uppdateringar varje gång den startar
if check_for_updates():
    # Starta om för att ladda ny kod
    import machine
    machine.reset()
else:
    # Kör lokal version
    import rgb_control