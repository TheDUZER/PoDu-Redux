import pickle, os, imgkit

class PokemonList():
    def __init__(self):
        pass
    def __iter__(self):
        counter = 0
        __iterator = iter(self.__dict__.values())
        return __iterator
    
    def __next__(self):
        if counter == len(self.__dict__.values()):
            counter = 0
            raise StopIteration
        else:
            counter += 1
            return __iterator

    def __str__(self):
        return self.Name

class Pokemon():
    def __init__(self, line = None):
        pass
    """
        self.Attacks = Attacks()

        pkmn_stat_dict = PKMN_STATS[line]
        for keys, values in pkmn_stat_dict.items():
            new_keys = keys[0].upper() + keys[1:]
            if keys.startswith('attack') == False:
                setattr(self, f"{new_keys}", values)
        for keys, values in pkmn_stat_dict.items():
            new_keys = keys[0].upper() + keys[1:]
            if keys.startswith('attack'):
                new_attack_keys = keys[7].upper() + keys[8:]
                if new_attack_keys == 'Color' and values == None:
                    break
                if hasattr(self, "Attacks") == False:
                    setattr(
                        self, "Attacks", AttackList())
                if hasattr(
                    self.Attacks, f"Attack{keys[6]}") == False:
                    setattr(
                        self.Attacks, f"Attack{keys[6]}", Attacks())
                current_attack = getattr(
                    self.Attacks, f"Attack{keys[6]}")
                setattr(current_attack, new_attack_keys, values)
                if hasattr(current_attack, "Effect") == False:
                    setattr(current_attack, "Effect", None)
                if hasattr(current_attack, "Power") == False:
                    setattr(current_attack, "Power", None)
    """


    def __iter__(self):
        counter = 0
        __iterator = iter(self.__dict__.values())
        return __iterator
    
    def __next__(self):
        if counter == len(self.__dict__.values()):
            counter = 0
            raise StopIteration
        else:
            counter += 1
            return __iterator

    def __str__(self):
        return self.Name

class Attacks():
    def __init__(self):
        pass

    def __iter__(self):
        counter = 0
        __iterator = iter(self.__dict__.values())
        return __iterator
    
    def __next__(self):
        if counter == len(self.__dict__.values()):
            counter = 0
            raise StopIteration
        else:
            counter += 1
            return __iterator

class AttackList():
    def __init__(self):
        pass

    def __iter__(self):
        counter = 0
        __iterator = iter(self.__dict__.values())
        return __iterator
    
    def __next__(self):
        if counter == len(self.__dict__.values()):
            counter = 0
            raise StopIteration
        else:
            counter += 1
            return __iterator

config = imgkit.config(wkhtmltoimage=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe')
options = {'width': 265, 'disable-smart-width': ''}

style_string = """\
<style>
@font-face {
    font-family: 'pokemon_gbregular';
    src: url('/CustomFont/pokemon_gb-webfont.woff2') format('woff2'),
         url('CustomFont/pokemon_gb-webfont.woff') format('woff');
    font-weight: normal;
    font-style: normal;

}

.card {
    border-style: solid;
    border-width: 0.75mm;
    border-color: black;
    width: 64mm;
    height: 89mm; 
    font-size: 8.5px; 
    font-family: sans-serif;
}

.framesection1 {
    width: 30%;
    float: left;
}

.framesection2 {
    width: 20%;
    float: left;
}

.sprite{
    transform: rotateY(180deg);
    margin-left: 3px;
    margin-top: 3px;
    width: 40px;
    height: 40px;
    display: block;
    position: absolute;
}

.sprite2{
    margin-left: 198px;
    margin-top: 3px;
    width: 40px;
    height: 40px;
    display: block;
    position: absolute;
}

.sprite3{
    width: inherit;
    height: inherit;
    opacity: 0.2;
    display: block;
    z-index: -100;
    background-size: 256px 256px;
    position: absolute;
    background-repeat: no-repeat;
    background-position-x: center;
    background-position-y: 20mm;
}

.name {
    font-family: "pokemon_gbregular";
    float: top;
    margin-top: 1.5mm;
    font-size: 8px;
    text-justify: auto;
    margin-left: 2mm;
    margin-right: 2mm;
    text-align: center;
}

.cardtext {
    clear: left;
    float: left;
    text-align: left;
}

.attackframe{
    float: left;
    width: 62mm;
    border-style: hidden;
    border-width: 0.2mm;
    border-color: black;
    margin-left: 1mm;
    margin-right: 1mm;
}

.ability{
    background-color: rgb(160, 160, 160);
    border-style: solid;
    border-radius: 1mm;
    border-width: 0.4mm;
    margin-left: 1mm;
    margin-right: 1mm;
    padding: 0.2mm;
    width: 61mm;
}
</style>
"""
def do_work():      
    PkmnObjData = pickle.load(open("pkmn-stats.p", "rb"))

    for target in PkmnObjData:

        name = target.Name
        new_filename = "".join(filter(str.isalnum, target.Name))
        sprite_file = os.path.join("sprites", target.Spritefile)
        MP = target.Move
        type1file = os.path.join("TypeLabels", target.Type1 + ".png")
        type2file = os.path.join("TypeLabels", target.Type2 + ".png") if target.Type2 else ""
        evolutions = target.Evolutions if target.Evolutions else ""
        forms = target.Forms if target.Ability else ""
        ability = target.Ability if target.Ability else ""
        megafile = "mega.png" if ", Mega" in target.Name else ""
        if MP == 0:
            movefile = 'mp0.png'
        elif MP == 1:
            movefile = 'mp1.png'
        elif MP == 2:
            movefile = 'mp2.png'
        elif MP == 3:
            movefile = 'mp3.png'

        attackframe = ""

        for attack in target.Attacks:
            if attack.Color == "Blue":
                attack_color = "Aqua"
            elif attack.Color == "Purple":
                attack_color = "Mediumorchid"
            else:
                attack_color = attack.Color
            attack_name = attack.Name
            attack_range = attack.Range
            attack_size = attack.Size
            attack_power = attack.Power if attack.Power else ""
            attack_effect = attack.Effect if attack.Effect else ""
            attackframe_string = f"""\
                    <div class="attackframe" style="background-color:{attack_color}">
                        <div class="framesection1"><em><b>{attack_name}</b></em></div>
                        <div class="framesection2">Hit: <b>{attack_range}</b></div>
                        <div class="framesection2">Size: <b>{attack_size}</b></div>
                        <div class="framesection1">Power: <b>{attack_power}</b></div>
                        {attack_effect}
                    </div>\n"""
            attackframe += "\n" + attackframe_string

        html_string = f"""\
        <!doctype html>
        <html>
           
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"></meta>
            {style_string}
        </head>

        <body>
            <div class="card">
                <div class="sprite"><img src="{sprite_file}"></div>
                <div class="sprite2"><img src="{sprite_file}"></div>
                <div class="cardtext">   
                    <div class="name">
                        {name}
                    </div>
                    <div class="name">
                        <img src="{movefile}" width=14px height=14px><img src="{type1file}"><img src="{type2file}"><img src="{megafile}">
                    </div>     
                    <br>
                    <div class="ability">
                        <em>Evolutions:</em> {evolutions}
                        <br>
                        <em>Forms:</em> {forms}
                        <br>
                        <em>Ability:</em> {ability}
                    </div>
                    {attackframe}
                </div>
            </div>
        </body

        </html>"""

        with open(os.path.join("new_html", new_filename + ".html"), "w+") as new_file:
            new_file.write(html_string)
            new_file.close()
        imgkit.from_file(os.path.join("new_html", new_filename + ".html"),
                         os.path.join("new_html", "new_images", target.Spritefile[:-4] + "_card.png"), options=options, config=config)

