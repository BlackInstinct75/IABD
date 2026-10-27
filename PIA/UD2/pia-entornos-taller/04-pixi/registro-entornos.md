04-pixi

(base) PS C:\Users\ia\Desktop\IABD\PIA\UD2\pia-entornos-taller\04-pixi> pixi --version
pixi 0.80.0
(base) PS C:\Users\ia\Desktop\IABD\PIA\UD2\pia-entornos-taller\04-pixi> pixi init .
Created C:\Users\ia\Desktop\IABD\PIA\UD2\pia-entornos-taller\04-pixi\pixi.toml
(base) PS C:\Users\ia\Desktop\IABD\PIA\UD2\pia-entornos-taller\04-pixi> pixi add "python=3.12" "pandas>=2.2,<3"
Added python=3.12
Added pandas>=2.2,<3
(base) PS C:\Users\ia\Desktop\IABD\PIA\UD2\pia-entornos-taller\04-pixi> pixi run python analisis.py
Python: C:\Users\ia\Desktop\IABD\PIA\UD2\pia-entornos-taller\04-pixi\.pixi\envs\default\python.exe
pandas: 2.3.3
Total: 60
Por grupo: {'A': 30, 'B': 30}
PRUEBA OK
(base) PS C:\Users\ia\Desktop\IABD\PIA\UD2\pia-entornos-taller\04-pixi> 

[workspace]
authors = ["BlackInstinct75 <franciscoborge249@gmail.com>"]
channels = ["conda-forge"]
name = "04-pixi"
platforms = ["win-64"]
version = "0.1.0"

[tasks]

[dependencies]
python = "3.12.*"
pandas = ">=2.2,<3"

(base) PS C:\Users\ia\Desktop\IABD\PIA\UD2\pia-entornos-taller\04-pixi> ls


    Directorio: C:\Users\ia\Desktop\IABD\PIA\UD2\pia-entornos-taller\04-pixi


Mode                 LastWriteTime         Length Name                                                    
----                 -------------         ------ ----                                                    
d-----        27/10/2026     16:58                .pixi                                                   
-a----        27/10/2026     16:58            128 .gitattributes                                          
-a----        27/10/2026     16:58             47 .gitignore                                              
-a----        27/10/2026     16:35            430 analisis.py                                             
-a----        27/10/2026     16:58          19828 pixi.lock                                               
-a----        27/10/2026     17:00            220 pixi.toml                                               
-a----        27/10/2026     17:02            995 registro-entornos.md                                    


(base) PS C:\Users\ia\Desktop\IABD\PIA\UD2\pia-entornos-taller\04-pixi> ls .\.pixi\envs\default\ "python*" 
   

    Directorio: C:\Users\ia\Desktop\IABD\PIA\UD2\pia-entornos-taller\04-pixi\.pixi\envs\default


Mode                 LastWriteTime         Length Name                                                    
----                 -------------         ------ ----                                                    
-a----        26/10/2026     12:29          93184 python.exe                                              
-a----        26/10/2026     12:31         552960 python.pdb                                              
-a----        26/10/2026     12:29          56320 python3.dll                                             
-a----        26/10/2026     12:30        7425024 python312.dll                                           
-a----        26/10/2026     12:31       17854464 python312.pdb                                           
-a----        26/10/2026     12:29          91648 pythonw.exe                                             
-a----        26/10/2026     12:31         569344 pythonw.pdb                                             


(base) PS C:\Users\ia\Desktop\IABD\PIA\UD2\pia-entornos-taller\04-pixi> 

(base) PS C:\Users\ia\Desktop\IABD\PIA\UD2\pia-entornos-taller\04-pixi> pixi run python analisis.py
Python: C:\Users\ia\Desktop\IABD\PIA\UD2\pia-entornos-taller\04-pixi\.pixi\envs\default\python.exe
pandas: 2.3.3
Total: 60
Por grupo: {'A': 30, 'B': 30}
PRUEBA OK
(base) PS C:\Users\ia\Desktop\IABD\PIA\UD2\pia-entornos-taller\04-pixi> 


(base) PS C:\Users\ia\Desktop\IABD\PIA\UD2\pia-entornos-taller\04-pixi> pixi task add analizar "python analisis.py"
Added task `analizar`: python analisis.py
(base) PS C:\Users\ia\Desktop\IABD\PIA\UD2\pia-entornos-taller\04-pixi> pixi run analizar
Pixi task (analizar): python analisis.py
Python: C:\Users\ia\Desktop\IABD\PIA\UD2\pia-entornos-taller\04-pixi\.pixi\envs\default\python.exe
pandas: 2.3.3
Total: 60
Por grupo: {'A': 30, 'B': 30}
PRUEBA OK
(base) PS C:\Users\ia\Desktop\IABD\PIA\UD2\pia-entornos-taller\04-pixi> pixi add rich
Added rich >=15.0.0,<16
(base) PS C:\Users\ia\Desktop\IABD\PIA\UD2\pia-entornos-taller\04-pixi> pixi run python -c "from rich import print; print('[green]Pixi listo[/green]')"
Pixi listo
(base) PS C:\Users\ia\Desktop\IABD\PIA\UD2\pia-entornos-taller\04-pixi> pixi run analizar
Pixi task (analizar): python analisis.py
Python: C:\Users\ia\Desktop\IABD\PIA\UD2\pia-entornos-taller\04-pixi\.pixi\envs\default\python.exe
pandas: 2.3.3
Total: 60
Por grupo: {'A': 30, 'B': 30}
PRUEBA OK
(base) PS C:\Users\ia\Desktop\IABD\PIA\UD2\pia-entornos-taller\04-pixi> 