def configs():
    cfgfile = open("config.cfg", 'w')
    Config = configparser.ConfigParser()
    # add the settings to the structure of the file, and lets write it out...
    Config.add_section('misp')
    Config.set('misp', 'url', 'https://localhost:8443')
    Config.set('misp', 'key', 'keyhere')
    Config.set('misp', 'verify_cert', 'False')

    Config.add_section('resilient')
    Config.set('resilient', 'org', 'GSMA')
    Config.set('resilient', 'port', '443')
    Config.set('resilient', 'email', 'ayooluokun@outlook.com')
    Config.set('resilient', 'password', 'pws')
    Config.set('resilient', 'host ', 'gsma.resilientsystems.com')
    Config.write(cfgfile)

if __name__="__main__":
    configs()