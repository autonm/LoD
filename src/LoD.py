import cmd

RELEASE = "0.28072016"


class Country:
    app = None
    name = ""
    control = ""
    posture = 0
    # TODO this needs changing to an enum ?
    # Active Support = -2
    # Passive Support = -1
    # Neutral = 0
    # Passive Opposition = 1
    # Active Opposition = 2
    british_regular = 0
    british_tories = 0
    british_fort = 0
    british_howe = False
    patriot_continental = 0
    patriot_militia = 0
    patriot_fort = 0
    patriot_militia_active = 0
    patriot_washington = False
    indian_war_party = 0
    indian_village = 0
    indian_war_party_active = 0
    indian_brant = False
    french_blockade = 0
    french_regular = 0
    is_muster = False
    is_battle = False
    propaganda = 0

    def __init__(self, theapp, thename, thecontrol, theposture, thebritish_regular, thebritish_tories, thebritish_fort, thebritish_howe, thepatriot_continental, thepatriot_militia, thepatriot_fort, thepatriot_militia_active, thepatriot_washington, theindian_war_party, theindian_village, theindian_war_party_active, theindian_brant, thefrench_squadron, thefrench_regular, theis_muster, theis_battle, thepropaganda):
        self.app = theapp
        self.name = thename
        self.control = thecontrol
        self.posture = theposture
        self.british_regular = thebritish_regular
        self.british_tories = thebritish_tories
        self.british_howe = thebritish_howe
        self.british_fort = thebritish_fort
        self.patriot_continental = thepatriot_continental
        self.patriot_militia = thepatriot_militia
        self.patriot_fort = thepatriot_fort
        self.patriot_militia_active = thepatriot_militia_active
        self.patriot_washington = thepatriot_washington
        self.indian_war_party = theindian_war_party
        self.indian_village = theindian_village
        self.indian_war_party_active = theindian_war_party_active
        self.indian_brant = theindian_brant
        self.french_squadron = thefrench_squadron
        self.french_regular = thefrench_regular
        self.is_muster = theis_muster
        self.is_battle = theis_battle
        self.propaganda = thepropaganda


class LoD(cmd.Cmd):
    scenario = 0
    campaign = 1
    yearfrom = 0
    yearto = 0
    currentyear = 0

    ToA_Played = False

    total_support = 0
    total_opposition = 0
    french_preparations = 0
    cbc = 0
    crc = 0
    fni_level = 0

    british_forts_casualty = 0
    british_regular_casualty = 0
    british_torie_casualty = 0
    patriot_continental_casualty = 0
    french_regular_casualty = 0

    british_resources = 0
    british_regular_available = 0
    british_tories_available = 0
    british_forts_available = 0
    british_regular_unavailable = 0
    british_tories_unavailable = 0
    british_release_date = 0
    british_release_regulars = 0
    british_release_tories = 0

    patriot_resources = 0
    patriot_continental_available = 0
    patriot_militia_available = 0
    patriot_forts_available = 0
    patriot_forts_casualty = 0

    indians_war_parties_available = 0
    indian_villages_available = 0
    indians_resources = 0

    french_resources = 0
    french_regular_unavailable = 0
    french_regular_available = 0
    french_squadron_unavailable = 0
    french_squadron_available = 0
    french_rochambeau_available = False

    currentcard = 0
    currentcardfaction = ""
    currenteventfaction = ""
    currentevent = ""
    pass_turn = False
    french_skirmish_loop = False
    french_naval_pressure_loop = False

    map = {}
    cards = {}

    def __init__(self, thescenario):
        cmd.Cmd.__init__(self)
        self.scenario = thescenario
        self.scenariosetup()
        self.map = {}
        self.mapsetup()

        print "french_flow, map, toa, fni, map, status [country], status scenario, status"
        print ""
        self.prompt = "Command: "

    def postcmd(self, stop, line):
        if line == "quit":
            return True

    def help_quit(self):
        print "Quits game."

    def emptyline(self):
        print ""
        print 'Year: %s' % self.currentyear
        print 'Enter help for a list of commands.'

    def scenariosetup(self):
        print ""
        print 'Running scenariosetup: %s' % self.scenario
        if self.scenario == 1:
            self.campaign = 1
        elif self.scenario == 2:
            self.campaign = 1
            self.yearfrom = 1776
            self.yearto = 1779
            self.currentyear = 1776

            self.british_resources = 5
            self.patriot_resources = 2
            self.french_resources = 5
            self.indians_resources = 0
            self.total_support = 3
            self.total_opposition = 5
            self.cbc = 1  # Cumulative British Casulaties
            self.crc = 3  # Cumulative Rebellion Casulaties
            self.fni_level = 0
            self.french_preparations = 9

            self.british_regular_available = 7
            self.british_tories_available = 10
            self.british_forts_available = 3

            self.patriot_continental_available = 12
            self.patriot_militia_available = 10
            self.patriot_forts_available = 4

            self.french_regular_available = 6
            self.french_rochambeau_available = True

            self.indians_war_parties_available = 7
            self.indian_villages_available = 10

            self.british_regular_unavailable = 6
            self.british_tories_unavailable = 6

            self.french_regular_unavailable = 9
            self.french_squadron_unavailable = 1

            self.british_release_date = 1776
            self.british_release_regulars = 6
            self.british_release_tories = 6

    def mapsetup(self):
        print ""
        print 'Running mapsetup: %s' % self.scenario
        if self.scenario == 1:
            self.scenario = 1
        elif self.scenario == 2:
            self.map["QC"] = Country(self, "Quebec City", "British Control", -1, 1, 1, 0, False, 0, 0, 0, 0, False, 0, 0, 0, False, 0, 0, False, False, 0)
            self.map["B"] = Country(self, "Boston", "Uncontrolled", 1, 0, 0, 0, False, 0, 0, 0, 0, False, 0, 0, 0, False, 0, 0, False, False, 0)
            self.map["NYC"] = Country(self, "New York City", "British Control", -1, 6, 0, 1, True, 1, 0, 0, 0, False, 0, 0, 0, False, 0, 0, False, False, 0)
            self.map["PHIL"] = Country(self, "Philadelphia", "Rebellion Control", 0, 0, 0, 0, False, 0, 1, 0, 0, False, 0, 0, 0, False, 0, 0, False, False, 0)
            self.map["CT"] = Country(self, "Charles Town", "Rebellion Control", 0, 0, 0, 0, False, 2, 0, 1, 0, False, 0, 0, 0, False, 0, 0, False, False, 0)
            self.map["Q"] = Country(self, "Quebec", "British Control", 0, 1, 1, 1, False, 0, 1, 0, 0, False, 1, 1, 0, False, 0, 0, False, False, 0)
            self.map["NW"] = Country(self, "Northwest", "Uncontrolled", 0, 0, 0, 0, False, 0, 0, 0, 0, False, 1, 0, 0, False, 0, 0, False, False, 0)
            self.map["SW"] = Country(self, "Southwest", "Uncontrolled", 0, 0, 0, 0, False, 0, 0, 0, 0, False, 1, 1, 0, False, 0, 0, False, False, 0)
            self.map["F"] = Country(self, "Florida", "British Control", 0, 1, 0, 1, False, 0, 0, 0, 0, False, 2, 0, 0, False, 0, 0, False, False, 0)
            self.map["M"] = Country(self, "Massachusetts", "Rebellion Control", 2, 0, 0, 0, False, 1, 1, 1, 0, False, 0, 0, 0, False, 0, 0, False, False, 0)
            self.map["NY"] = Country(self, "New York", "British Control", 0, 3, 3, 0, False, 3, 0, 0, 0, True, 2, 0, 0, True, 0, 0, False, False, 0)
            self.map["V"] = Country(self, "Virginia", "British Control", 0, 0, 2, 0, False, 0, 0, 0, 0, False, 0, 0, 0, False, 0, 0, False, False, 0)
            self.map["NC"] = Country(self, "North Carolina", "Rebellion Control", 0, 0, 0, 0, False, 1, 1, 0, 0, False, 1, 0, 0, False, 0, 0, False, False, 0)
            self.map["SC"] = Country(self, "South Carolina", "British Control", 0, 0, 2, 0, False, 0, 0, 0, 0, False, 0, 0, 0, False, 0, 0, False, False, 0)
            self.map["G"] = Country(self, "Georgia", "Rebellion Control", 0, 0, 0, 0, False, 0, 1, 0, 0, False, 0, 0, 0, False, 0, 0, False, False, 0)
            self.map["WI"] = Country(self, "West Indies", "Rebellion Control", 0, 0, 0, 0, False, 0, 0, 0, 0, False, 0, 0, 0, False, 2, 0, False, False, 0)
            self.map["S"] = Country(self, "Savannah", "Uncontrolled", 0, 0, 0, 0, False, 0, 0, 0, 0, False, 0, 0, 0, False, 0, 0, False, False, 0)
            self.map["NH"] = Country(self, "New Hampshire", "Uncontrolled", 0, 0, 0, 0, False, 0, 0, 0, 0, False, 0, 0, 0, False, 0, 0, False, False, 0)
            self.map["N"] = Country(self, "Norfolk", "Uncontrolled", 0, 0, 0, 0, False, 0, 0, 0, 0, False, 0, 0, 0, False, 0, 0, False, False, 0)
            self.map["NJ"] = Country(self, "New Jersey", "Uncontrolled", 0, 0, 0, 0, False, 0, 0, 0, 0, False, 0, 0, 0, False, 0, 0, False, False, 0)
            self.map["ML"] = Country(self, "Maryland", "Uncontrolled", 0, 0, 0, 0, False, 0, 0, 0, 0, False, 0, 0, 0, False, 0, 0, False, False, 0)
            self.map["PEN"] = Country(self, "Penns", "Uncontrolled", 0, 0, 0, 0, False, 0, 0, 0, 0, False, 0, 0, 0, False, 0, 0, False, False, 0)
            self.map["C"] = Country(self, "Connect", "Uncontrolled", 0, 0, 0, 0, False, 0, 0, 0, 0, False, 0, 0, 0, False, 0, 0, False, False, 0)

    def control_change_check(self):
        print ""
        print "Checking Control Changes...."
        for country in self.map:
            rebellion_control = int(self.map[country].patriot_continental) + int(self.map[country].patriot_militia) + int(self.map[country].patriot_fort) + int(self.map[country].patriot_militia_active)
            rebellion_control += int(self.map[country].french_regular)

            british_count = int(self.map[country].british_tories) + int(self.map[country].british_regular) + int(self.map[country].british_fort)
            indian_count = int(self.map[country].indian_war_party) + int(self.map[country].indian_village) + int(self.map[country].indian_war_party_active)

            if rebellion_control > british_count + indian_count:
                if self.map[country].control != "Rebellion Control":
                    print "ACTION: Control changed in: %s from %s to Rebellion Control" % (self.map[country].name, self.map[country].control)
                    self.map[country].control = "Rebellion Control"

            elif british_count + indian_count >= rebellion_control and british_count > 0:
                if self.map[country].control != "British Control":
                    print "ACTION: Control changed in: %s from %s to British Control" % (self.map[country].name, self.map[country].control)
                    self.map[country].control = "British Control"

                if indian_count >= rebellion_control and british_count == 0:
                    print "ACTION: Control changed in: %s from %s to Uncontrolled" % (self.map[country].name, self.map[country].control)
                    self.map[country].control = "Uncontrolled"

        print "Control Change Complete."
        print ""

    def do_status(self, rest):

        if rest == 'scenario':
            print ""
            print "*Scenario Status Report*"
            print "Scenario: %s" % self.scenario
            print "Campaign: %s" % self.campaign
            print "Year From: %s" % self.yearfrom
            print "Year To: %s" % self.yearto
            print "Current Year: %s" % self.currentyear
            return

        elif rest:
            print ""
            goodcountry = False
            possible = []
            for country in self.map:
                if rest.lower() == country.lower():
                    possible = []
                    possible.append(country)
                    break
                elif rest.lower() in country.lower():
                    possible.append(country)
            if len(possible) == 0:
                print "Unrecognized country."
                print ""
            elif len(possible) > 1:
                print "Be more specific", possible
                print ""
            else:
                goodcountry = possible[0]

            if goodcountry:
                print '*Location Status Report*'
                print 'Name: %s' % self.map[goodcountry].name
                print 'Control: %s' % self.map[goodcountry].control
                print "** Active Support = -2, Passive Support = -1, Neutral = 0, Passive Opposition = 1, Active Opposition = 2 **"
                print 'Posture is %s' % self.map[goodcountry].posture
                print 'British Regulars: %s' % self.map[goodcountry].british_regular
                print 'British Tories: %s' % self.map[goodcountry].british_tories
                print 'British Fort: %s' % self.map[goodcountry].british_fort
                print 'British Howe: %s' % self.map[goodcountry].british_howe
                print 'Patriots Continental: %s' % self.map[goodcountry].patriot_continental
                print 'Patriots Militia Underground: %s' % self.map[goodcountry].patriot_militia
                print 'Patriots Militia Active: %s' % self.map[goodcountry].patriot_militia_active
                print 'Patriots Fort: %s' % self.map[goodcountry].patriot_fort
                print 'Patriots Washington: %s' % self.map[goodcountry].patriot_washington
                print 'Indians War Party Underground: %s' % self.map[goodcountry].indian_war_party
                print 'Indians War Party Active: %s' % self.map[goodcountry].indian_war_party_active
                print 'Indians Village: %s' % self.map[goodcountry].indian_village
                print 'Indians Brant: %s' % self.map[goodcountry].indian_brant
                print 'French Blockades: %s' % self.map[goodcountry].french_squadron
                print 'Propaganda [1:True; 0:False]: %s' % self.map[goodcountry].propaganda
                print ""

                return
            else:
                return

        for country in self.map:
            print ""
            print 'Name %s' % self.map[country].name

            if self.map[country].control != "":
                print 'Control: %s' % self.map[country].control

            if self.map[country].posture != "":
                print 'Posture: %s' % self.map[country].posture

            if self.map[country].british_regular > 0:
                print 'British Regulars: %s' % self.map[country].british_regular

            if self.map[country].british_tories > 0:
                print 'British Tories: %s' % self.map[country].british_tories

            if self.map[country].british_fort > 0:
                print 'British Fort: %s' % self.map[country].british_fort

            if self.map[country].british_howe == True:
                print 'British Howe: %s' % self.map[country].british_howe

            if self.map[country].patriot_continental > 0:
                print 'Patriots Continental: %s' % self.map[country].patriot_continental

            if self.map[country].patriot_militia > 0:
                print 'Patriots Militia: %s' % self.map[country].patriot_militia

            if self.map[country].patriot_fort > 0:
                print 'Patriots Fort: %s' % self.map[country].patriot_fort

            if self.map[country].patriot_washington == True:
                print 'Patriots Washington: %s' % self.map[country].patriot_washington

            if self.map[country].indian_war_party > 0:
                print 'Indians War Party: %s' % self.map[country].indian_war_party

            if self.map[country].indian_village > 0:
                print 'Indians Village: %s' % self.map[country].indian_village

            if self.map[country].indian_brant == True:
                print 'Indians Brant: %s' % self.map[country].indian_brant

            if self.map[country].french_squadron > 0:
                print 'French Squadrons: %s' % self.map[country].french_squadron

        print ""
        print "French Regulars Available: %s" % self.french_regular_available
        print "French Regulars Un-Available: %s" % self.french_regular_unavailable
        print "French Squadron Un-Available: %s" % self.french_squadron_unavailable

    def help_status(self):
        print 'Display game status.'
        print "status [country] - status display of single country."
        print "status scenario - display scenario information."
        print ""

    def do_fni(self,rest):
        print ""
        self.fni_level = raw_input("FNI Level [" + str(self.fni_level) + "] Change to [0-3] ? ")

    def do_toa(self,rest):
        print ""
        self.ToA_Played = raw_input("ToA Played [" + str(self.ToA_Played) + "] Change to [True, False] ? ")

    def do_total_opp(self,rest):
        print ""
        self.total_opposition = raw_input("Change Total Opposition [" + str(self.total_opposition) + "] Change to [0-100] : ")

    def do_total_support(self,rest):
        print ""
        self.total_support = raw_input("Change Total Support [" + str(self.total_support) + "] Change to [0-100] : ")

    def do_french_prep(self,rest):
        print ""
        self.french_preparations = raw_input("Change French Preparations [" + str(self.french_preparations) + "] Change to [0-100] : ")

    def do_crc(self,rest):
        print ""
        self.crc = raw_input("Change Cumulative Rebellion Casulaties [" + str(self.crc) + "] Change to [0-100] : ")

    def do_cbc(self,rest):
        print ""
        self.cbc = raw_input("Change Cumulative British Casulaties [" + str(self.cbc) + "] Change to [0-100] : ")

    def do_british(self,rest):
        print ""
        self.british_resources = raw_input("Change British Resources [" + str(self.british_resources) + "] Change to [0-100] : ")

    def do_patriot(self,rest):
        print ""
        self.patriot_resources = raw_input("Change Patriot Resources [" + str(self.patriot_resources) + "] Change to [0-100] : ")

    def do_french(self,rest):
        print ""
        self.french_resources = raw_input("Change French Resources [" + str(self.french_resources) + "] Change to [0-100] : ")

    def do_indian(self,rest):
        print ""
        self.indians_resources = raw_input("Change Indian Resources [" + str(self.indians_resources) + "] Change to [0-100] : ")

    def do_map(self, rest):
        try:
            print "Map Codes:"
            print "[B] Boston, [CT] Charles Town, [C] Connect, [F] Florida, [G]Georgia"
            print "[M] Massachusetts, [ML] Maryland, [N] Norfolk, [NC] North Carolina"
            print "[NH] New Hampshire, [NJ] New Jersey, [NW] Northwest, [NY] New York"
            print "[NYC] New York City, [PEN] Penns, [PHIL] Philadelphia, [Q] Quebec"
            print "[QC] Quebec City, [S] Savannah, [SC] South Carolina, [SW] Southwest"
            print "[V] Virginia, [WI] West Indies"
            print ""

            country = raw_input("Enter location to change: ").upper()
            print ""
            print 'Name: %s' % self.map[country].name
            print 'Control: %s' % self.map[country].control

            print "** Active Support = -2, Passive Support = -1, Neutral = 0, Passive Opposition = 1, Active Opposition = 2 **"
            self.map[country].posture = raw_input("Posture [" + str(self.map[country].posture) + "] Change to [-2,-1,0,1,2] ? ")
            self.map[country].british_regular = raw_input("British Regulars [" + str(self.map[country].british_regular) + "] Change to [0-100] : ")
            self.map[country].british_tories = raw_input("British Tories [" + str(self.map[country].british_tories) + "] Change to [0-100] : ")
            self.map[country].british_fort = raw_input("British Fort [" + str(self.map[country].british_fort) + "] Change to [0-100] : ")
            self.map[country].british_howe = raw_input("British Howe [" + str(self.map[country].british_howe) + "] Change to [True/False] : ")
            self.map[country].patriot_continental = raw_input("Patriots Continental [" + str(self.map[country].patriot_continental) + "] Change to [0-100] : ")
            self.map[country].patriot_militia = raw_input("Patriots Militia Underground [" + str(self.map[country].patriot_militia) + "] Change to [0-100] : ")
            self.map[country].patriot_militia_active = raw_input("Patriots Militia Active [" + str(self.map[country].patriot_militia_active) + "] Change to [0-100] : ")
            self.map[country].patriot_fort = raw_input("Patriots Fort [" + str(self.map[country].patriot_fort) + "] Change to [0-100] : ")
            self.map[country].patriot_washington = raw_input("Patriots Washington [" + str(self.map[country].patriot_washington) + "] Change to [True/False] : ")
            self.map[country].indian_war_party = raw_input("Indians War Party Underground [" + str(self.map[country].indian_war_party) + "] Change to [0-100] : ")
            self.map[country].indian_war_party_active = raw_input("Indians War Party Active [" + str(self.map[country].indian_war_party_active) + "] Change to [0-100] : ")
            self.map[country].indian_village = raw_input("Indians Villages [" + str(self.map[country].indian_village) + "] Change to [0-100] : ")
            self.map[country].indian_brant = raw_input("Indians Brant [" + str(self.map[country].indian_brant) + "] Change to [True/False] : ")
            self.map[country].french_squadron = raw_input("French Blockade [" + str(self.map[country].french_squadron) + "] Change to [0-100] : ")
            self.map[country].propaganda = raw_input("Propaganda [" + str(self.map[country].propaganda) + "] Change to [1 = True; 0 = False] : ")

            print ""
            self.control_change_check()
        except:
            print "Unknown location. Enter command again."

    def do_french_flow(self, rest):
        self.french_skirmish_loop = False
        self.french_naval_pressure_loop = False
        self.pass_turn = False

        if self.french_resources == 0:  # French can't play event and no resources
            print "FRENCH RESOURCES > 0?"
            print "French PASS as resources = 0"
            print "ACTION: Move French into PASS Box"

        else:
            print "FRENCH RESOURCES > 0?"
            print "French have %s resources, so > 0 .. True" % self.french_resources

            print ""
            print "TREATY OF ALLIANCE PLAYED?"
            print "Checking if ToA been played? %s " % self.ToA_Played

            if self.ToA_Played == False:
                self.french_patriot_resources_check()
            else:
                print ""
                print "ToA has been played"
                print "1D6 < AVAILABLE FRENCH REGULARS '%s' ?" % self.french_regular_available
                roll = input("ACTION: Enter 1D6 result:")

                if roll < self.french_regular_available:
                    self.french_muster()
                else:
                    print ""
                    print "REBEL CUBES + LEADER > BRITISH with PIECES IN SPACE WITH BOTH ?"
                    bfound = False

                    for country in self.map:
                        rebellion_cubes = int(self.map[country].patriot_continental) + int(self.map[country].french_regular)
                        if int(self.map[country].patriot_washington) == 1:
                            rebellion_cubes += 1

                        british_pieces = int(self.map[country].british_tories) + int(self.map[country].british_regular) + int(self.map[country].british_fort)
                        if rebellion_cubes > british_pieces:
                            bfound = True
                            print "Location match of %s (Rebellion Cubes %s) (British Pieces %s)" % (self.map[country].name, rebellion_cubes, british_pieces)

                    if bfound == False:
                        self.french_march()
                    else:
                        self.french_battle()

            self.pass_turn = False

    def french_patriot_resources_check(self):
        try:
            print ""
            print "PATRIOT RESOURCES < 1D3 ?"
            print "US Patriot Resources '%s' < 1D3 check" % self.patriot_resources
            roll = input("ACTION: Enter 1D3 result:")

            if self.patriot_resources >= roll:

                print ""
                print "FRENCH AGENT MOBILIZATION"
                # French Agent Mobilization
                if self.patriot_militia_available >= 2:
                    print ""
                    print "'%s' Patriot Militia Available. Place 2 Patriot Militia." % self.patriot_militia_available
                    print "Select 1st to add most Rebel Control - then where most Patriot Units"
                    print "Below is status of QC, NY, NH, MA"
                    print ""

                    print "Quebec is under %s" % self.map["QC"].control
                    if self.map["QC"].control == "Rebellion Control":
                        print "Quebec already Rebellion, unable to switch"
                        print ""
                    else:
                        rebellion_count = int(self.map["QC"].patriot_continental) + int(self.map["QC"].patriot_militia) + int(self.map["QC"].patriot_fort) + int(self.map["QC"].patriot_militia_active)
                        rebellion_count += int(self.map["QC"].french_regular)

                        royalist_count = int(self.map["QC"].british_tories) + int(self.map["QC"].british_regular) + int(self.map["QC"].british_fort)
                        royalist_count += int(self.map["QC"].indian_war_party) + int(self.map["QC"].indian_village) + int(self.map["QC"].indian_war_party_active)

                        patriot_count = self.map["QC"].patriot_militia + self.map["QC"].patriot_fort + self.map["QC"].patriot_continental + int(self.map["QC"].patriot_militia_active)
                        print "Quebec Rebellion (Patriot & French) combined = %s" % rebellion_count
                        print "Quebec Royalist (British & Indian) combined = %s" % royalist_count

                        if rebellion_count + 2 > royalist_count:
                            print "Adding 2 Militia to QC would change to Rebel Control !!"
                        else:
                            print "Adding 2 Militia to QC would NOT change to Rebel Control"
                            print "Quebec Patriot Count = %s" % patriot_count

                    print ""
                    print "New York is under %s" % self.map["NY"].control
                    if self.map["NY"].control == "Rebellion Control":
                        print "New York already Rebellion, unable to switch"
                        print ""
                    else:
                        rebellion_count = int(self.map["NY"].patriot_continental) + int(self.map["NY"].patriot_militia) + int(self.map["NY"].patriot_fort) + int(self.map["NY"].patriot_militia_active)
                        rebellion_count += int(self.map["NY"].french_regular)

                        royalist_count = int(self.map["NY"].british_tories) + int(self.map["NY"].british_regular) + int(self.map["NY"].british_fort)
                        royalist_count += int(self.map["NY"].indian_war_party) + int(self.map["NY"].indian_village) + int(self.map["NY"].indian_war_party_active)

                        patriot_count = self.map["NY"].patriot_militia + self.map["NY"].patriot_fort + self.map["NY"].patriot_continental + int(self.map["NY"].patriot_militia_active)
                        print "New York Rebellion (Patriot & French) combined = %s" % rebellion_count
                        print "New York Royalist (British & Indian) combined = %s" % royalist_count

                        if rebellion_count + 2 > royalist_count:
                            print "Adding 2 Militia to New York would change to Rebel Control !!"
                        else:
                            print "Adding 2 Militia to New York would NOT change to Rebel Control"
                            print "New York Patriot Count = %s" % patriot_count

                    print ""
                    print "New Hampshire is under %s" % self.map["NH"].control
                    if self.map["NH"].control == "Rebellion Control":
                        print "New Hampshire already Rebellion, unable to switch"
                        print ""
                    else:
                        rebellion_count = int(self.map["NH"].patriot_continental) + int(self.map["NH"].patriot_militia) + int(self.map["NH"].patriot_fort) + int(self.map["NH"].patriot_militia_active)
                        rebellion_count += int(self.map["NH"].french_regular)

                        royalist_count = int(self.map["NH"].british_tories) + int(self.map["NH"].british_regular) + int(self.map["NH"].british_fort)
                        royalist_count += int(self.map["NH"].indian_war_party) + int(self.map["NH"].indian_village) + int(self.map["NH"].indian_war_party_active)

                        patriot_count = self.map["NH"].patriot_militia + self.map["NH"].patriot_fort + self.map["NH"].patriot_continental + int(self.map["NH"].patriot_militia_active)
                        print "New Hampshire Rebellion (Patriot & French) combined = %s" % rebellion_count
                        print "New Hampshire (British & Indian) combined = %s" % royalist_count

                        if rebellion_count + 2 > royalist_count:
                            print "Adding 2 Militia to New Hampshire would change to Rebel Control !!"
                        else:
                            print "Adding 2 Militia to New Hampshire would NOT change to Rebel Control"
                            print "New Hampshire Patriot Count = %s" % patriot_count

                    print ""
                    print "Massachusetts is under %s" % self.map["M"].control
                    if self.map["M"].control == "Rebellion Control":
                        print "Massachusetts already Rebellion, unable to switch"
                        print ""
                    else:
                        rebellion_count = int(self.map["M"].patriot_continental) + int(self.map["M"].patriot_militia) + int(self.map["M"].patriot_fort) + int(self.map["M"].patriot_militia_active)
                        rebellion_count += int(self.map["M"].french_regular)

                        royalist_count = int(self.map["M"].british_tories) + int(self.map["M"].british_regular) + int(self.map["M"].british_fort)
                        royalist_count += int(self.map["M"].indian_war_party) + int(self.map["M"].indian_village) + int(self.map["M"].indian_war_party_active)

                        patriot_count = self.map["M"].patriot_militia + self.map["M"].patriot_fort + self.map["M"].patriot_continental + int(self.map["M"].patriot_militia_active)
                        print "Massachusetts Rebellion (Patriot & French) combined = %s" % rebellion_count
                        print "Massachusetts (British & Indian) combined = %s" % royalist_count

                        if rebellion_count + 2 > royalist_count:
                            print "Adding 2 Militia to Massachusetts would change to Rebel Control !!"
                        else:
                            print "Adding 2 Militia to Massachusetts would NOT change to Rebel Control"
                            print "Massachusetts Patriot Count = %s" % patriot_count

                    location = raw_input("Select Patriot Militia Location - [NONE]*Will goto Roderigue Hortalez* or [QC]Quebec [NY]New York [NH]New Hampshire [M]Massachusetts : ").upper()
                    if location.lower() == "none":
                        self.roderigue_hortalez()
                    else:
                        self.patriot_militia_available -= 2
                        self.map[location].patriot_militia += 2

                        print "Map & Available Counts updated"
                        print "ACTION: Move 2 Patriot Militia to %s " % location
                        print ""
                        self.control_change_check()

                        special = raw_input("Play Special Activity PREPARER la GUERRE ? [Y/N]")
                        if special.lower() == "y":
                            self.preparer_la_guerre()

                elif self.patriot_continental_available >= 1:
                    print "French Agent Mobilization as >=1 Patriot Continental Available, as < 2 Militia available"
                    location = raw_input("[Q]Quebec [NY]New York [NH]New Hampshire [M]Massachusetts - Select Patriot Militia Location: ").upper()
                    self.patriot_continental_available -= 1
                    self.map[location].patriot_continental += 1

                    print "Map & Available Counts updated"
                    print "ACTION: Move 1 Patriot Continental to %s " % location
                    print ""
                    self.control_change_check()

                else:
                    self.roderigue_hortalez()

                    if self.pass_turn == False:
                        self.preparer_la_guerre()

            else:
                self.roderigue_hortalez()
                if self.pass_turn == False:
                    self.preparer_la_guerre()
        except:
            print "Incorrect Action"

    def roderigue_hortalez(self):
        print ""
        print "RODERIGUE HORTALEX et CIE (TOA - %s )" % self.ToA_Played

        if self.ToA_Played == False:
            if self.french_resources > 0:
                print "Roll 1D3 for French Resources ('%s') to be added to Patriot Resources ('%s'):" % (self.french_resources, self.patriot_resources)
                roll = int(input("ACTION: Enter 1D3 result:"))
                if roll > self.patriot_resources:
                    print "Roll of %s was greater than available Patriot Resources. %s will be added" % roll, self.patriot_resources
                    roll = self.patriot_resources

                self.patriot_resources += roll
                self.french_resources -= roll
                print ""
                print "Resources updated"
                print "ACTION: Amend French Resources to '%s', Patriot Resources to '%s'" % (self.french_resources, self.patriot_resources)
                print ""

                special = raw_input("Play Special Activity PREPARER la GUERRE? [Y/N]")
                if special.lower() == "y":
                    self.preparer_la_guerre()

            else:
                print "French PASS as resources = 0"
                print "ACTION: Move French into PASS Box"
                print ""

    def preparer_la_guerre(self):
        print ""
        print "PREPARER la GUERRE (TOA - %s )" % self.ToA_Played

        if self.ToA_Played == False:
            if self.french_squadron_unavailable > 0:
                print "Unavailable French Squadron '%s'" % self.french_squadron_unavailable
                self.french_squadron_unavailable -= 1

                print "Map & Squadrons updated for WI"
                self.map["WI"].french_squadron += 1

                print "ACTION: Move 1 French Squadron to West Indies"
                print ""
            elif self.french_regular_unavailable > 0:

                    roll = input("ACTION: Enter number of French Regular Unavailable (max 3 or '%s') to move to Available :" % self.french_regular_unavailable )

                    self.french_regular_available += roll
                    self.french_regular_unavailable -= roll

                    print "(un)available Counts updated"
                    print "ACTION: Move %s French Regulars from Unavailable to Available" % roll
                    print ""

            else:
                print "No options available, no Special Event"

        else:
            print "1D6 < UNAVAILABLE FRENCH REGULARS '%s' + Blockades '%s' ?" % (self.french_regular_available, self.french_squadron_unavailable)
            roll = input("ACTION: Enter 1D6 result:")

            if roll <= self.french_regular_available + self.french_squadron_unavailable:
                if self.french_squadron_unavailable > 0:
                    self.map["WI"].french_squadron += 1
                    print ""
                    print "Map and counts updated"
                    print "ACTION: Move 1 Squadron/Blockade to WI"
                else:
                    print "Unable to move 1 Blockade to WI"
                    if self.french_regular_unavailable > 0:
                        print ""
                        print "MOVE UP TO 3 FRENCH REGULARS FROM UNAVILABLE TO AVAILABLE"
                        print "French Regulars in unavilable '%s'" % self.french_regular_unavailable
                        count = input("How many French Regulars to move ?")

                        self.french_regular_available += count
                        self.french_regular_unavailable -= count
                    elif self.french_regular_unavailable == 0 and self.french_resources == 0:
                        print ""
                        print "NO REGULARS OR BLOCKADES MOVED AND FRENCH RESOURCES = 0"
                        print "ACTION: +2 French resources"
                        print "Counts updated"
                        self.french_resources += 2
                    else:
                        if self.french_naval_pressure_loop == False:
                            self.french_naval_pressure()

    def french_muster(self):
        print ""
        print "MUSTER"
        print "French Regular Available '%s'" % self.french_regular_available
        print "WI is under %s" % self.map["WI"].control
        print ""

        self.french_skirmish_loop = True

        if self.french_regular_available < 4 and self.map["WI Indies"].control != "Rebellion Control":
            print "Muster in WI as < 4 Regulars & WI !Reb.Cont"
            print "ACTION: Move '%s' Available French Regulars to WI" % self.french_regular_available
            self.map["WI"].french_regular += self.french_regular_available
            self.map["WI"].is_muster = True
            self.french_regular_available = 0
        else:
            # Find Colony or City with Continentals AND Rebel Control, otherwise random location
            print "MUSTER first in a Colony or City with Continentals, then random."
            found = False
            for country in self.map:
                if (self.map[country].name != "Florida" and self.map[country].name != "Southwest" and self.map[country].name != "Northwest" and self.map[country].name != "Quebec") and self.map[country].patriot_continental > 0 and self.map[country].control == "Rebellion Control":
                    found = True
                    print "Option is %s, has '%s' Continentals under %s" % (self.map[country].name, self.map[country].patriot_continental, self.map[country].control)

            if found:
                location = raw_input("Enter short location code to Muster:").upper()
                print "ACTION: Move '%s' French Regulars to '%s' " % (self.french_regular_available, location)
                self.map[location].french_regular += self.french_regular_available
                self.map[location].is_muster = True
                self.french_regular_available = 0
            else:
                print "No Colony or City found with Continentals and Rebel Control"
                print "Checking for random options with Rebel Control"
                for country in self.map:
                    if (self.map[country].name != "Florida" and self.map[country].name != "Southwest" and self.map[country].name != "Northwest" and self.map[country].name != "Quebec") and self.map[country].control == "Rebellion Control":
                        found = True
                        print "Option is %s, under %s" % (self.map[country].name, self.map[country].control)

                if found:
                    print ""
                    location = raw_input("Enter short location code to Muster").upper()
                    print "ACTION: Move '%s' French Regulars to '%s' " % (self.french_regular_available, location)
                    self.map[location].french_regular += self.french_regular_available
                    self.map[location].is_muster = True
                    self.french_regular_available = 0
                else:
                    print ""
                    print "Unable to find location with Rebel Control...."
                    print ""
                    print "RODERIGUE HORTALEZ et CIE (after ToA)"
                    # No def for this, as it's always called in this sequence
                    if self.french_resources > 0:
                        print "Roll 1D3 for French Resources '%s' to be added to Patriot Resources '%s':" % (self.french_resources, self.patriot_resources)
                        roll = input("ACTION: Enter 1D3 result:")
                        self.patriot_resources += roll
                        self.french_resources -= roll
                        print "ACTION: Amend Resources French '%s', Patriot '%s'" % (self.french_resources, self.patriot_resources)
                    else:
                        print "RODERIGUE HORTALEZ et CIE not possible as French Resources = 0"

        # regardless call Skirmish
        self.french_skirmish()

    def french_skirmish(self):
        print ""
        print "SKIRMISH"

        if self.map["WI"].is_muster == False and self.map["WI"].is_battle == False and self.map["WI"].french_regular > 0 and (self.map["WI"].british_regular + self.map["WI"].british_tories) > 0:
            print "Skirmish in WI"
            print "WI Stats are as follows: %s" % self.map["WI"].is_muster
            print "WI Is Battle %s" % self.map["WI"].is_battle
            print "WI French Regular count %s" % self.map["WI"].french_regular
            print "WI British Regular count %s" % self.map["WI"].british_regular
            print "WI British Tories count %s" % self.map["WI"].british_tories
            print "WI British Fort count %s" % self.map["WI"].british_fort

            print ""
            print "Enter number(s) using the following rules:"
            print "1) Remove one British Fort + one French Regular, or"
            print "2) Remove as many British cubes as possible (if 2 cubes then also 1 French Regular)"
            print "WI has British Forts: %s, British Regular: %s, British Tory: %s, French Regular: %s" % (self.map["WI"].british_fort, self.map["WI"].british_regular, self.map["WI"].british_tories, self.map["WI"].french_regular)
            print ""

            british_fort = raw_input("Enter '1', if 1 British Fort can be removed, else 0:")

            if british_fort == 1:
                self.map["WI"].british_fort -= 1
                self.map["WI"].french_regular -= 1
                self.british_forts_casualty += 1
                self.french_regular_casualty += 1

                print ""
                print "Resource and Map updated"
                print "ACTION: Remove 1 British Fort from 'WI', place into Casulaties"
                print "ACTION: Remove 1 French Regular from 'WI', place into Casulaties"

            else:
                british_regular = raw_input("Enter number of British Regular Cubes to remove:")
                british_tory = raw_input("Enter number of British Tory Cubes to remove:")
                self.map["WI"].british_regular -= int(british_regular)
                self.british_regular_casualty += int(british_regular)
                self.map["WI"].british_tories -= int(british_tory)
                self.british_torie_casualty += int(british_tory)

                print ""
                print "Resource and Map updated"
                print "ACTION: Remove %s British Regular from 'WI', place into Casulaties" % (british_regular)
                print "ACTION: Remove %s British Tory from 'WI', place into Casulaties" % (british_tory)

                if british_regular + british_tory > 1:
                    self.map["WI"].french_regular -= 1
                    self.french_regular_casualty += 1
                    print "ACTION: Remove 1 French Regular from 'WI', place into Casulaties"

        else:   # unable to use WI, find somewhere else.
            print ""
            print "Unable to Skirmish in WI"
            print "WI Stats were as follows: %s" % self.map["WI"].is_muster
            print "WI Is Battle %s" % self.map["WI"].is_battle
            print "WI French Regular count %s" % self.map["WI"].french_regular
            print "WI British Regular count %s" % self.map["WI"].british_regular
            print "WI British Tories count %s" % self.map["WI"].british_tories
            print "WI British Fort count %s" % self.map["WI"].british_fort

            print ""
            print "Select space with both French & British pieces & NOT MUSTER/BATTLE"
            location = raw_input("Enter location initials for Skirmish or enter [NONE] for Preparer la Guerre:").upper()

            if location.lower() == "none":
                print "No available location...."
                print "....PREPARER la GUERRE"
                self.preparer_la_guerre()
            else:
                print ""
                print "Enter number(s) using the following rules:"
                print "1) Remove one British Fort + one French Regular, or"
                print "2) Remove as many British cubes as possible (if 2 cubes then also 1 French Regular)"
                print "'%s' has British Forts: %s, British Regular: %s, British Tory: %s, French Regular: %s" % (location, self.map["WI"].british_fort, self.map["WI"].british_regular, self.map["WI"].british_tories, self.map["WI"].french_regular)
                print ""

                british_fort = raw_input("Enter '1', if 1 British Fort can be removed, else 0:")

                if british_fort == 1:
                    self.map[location].british_fort -= 1
                    self.map[location].french_regular -= 1
                    self.british_forts_casualty += 1
                    self.french_regular_casualty += 1
                    print ""
                    print "Resource and Map updated"
                    print "ACTION: Remove 1 British Fort from '%s', place into Casulaties" % location
                    print "ACTION: Remove 1 French Regular from '%s', place into Casulaties" % location

                else:
                    british_regular = raw_input("Enter number of British Regular Cubes to remove:")
                    british_tory = raw_input("Enter number of British Tory Cubes to remove:")
                    self.map[location].british_regular -= int(british_regular)
                    self.british_regular_casualty += int(british_regular)
                    self.map[location].british_tories -= int(british_tory)
                    self.british_torie_casualty += int(british_tory)
                    print ""
                    print "Resource and Map updated"
                    print "ACTION: Remove %s British Regular from '%s', place into Casulaties" % (british_regular, location)
                    print "ACTION: Remove %s British Tory from '%s', place into Casulaties" % (british_tory, location)

                    if british_regular + british_tory > 1:
                        self.map[location].french_regular -= 1
                        self.french_regular_casualty += 1
                        print "ACTION: Remove 1 French Regular from '%s', place into Casulaties" % location

    def french_naval_pressure(self):

        self.french_naval_pressure_loop = True

        print ""
        print "NAVAL PRESSURE"
        print "First in city marked for Battle, then at city with most support"
        location = raw_input("Enter short location code to place blockade or NONE:").upper()

        if location.upper() != "NONE":
            print "Map and count updated"
            print "ACTION: Move blockade to %s" % location
            self.map[location].french_blockade += 1

        if self.french_skirmish_loop == False:
            self.french_skirmish()

    def french_march(self):
        print ""
        print "MARCH"
        print "Self select options:"
        print "Update using 'map' for all movements manually"

        self.french_skirmish_loop = True

        print ""
        option = raw_input("Enter choice: [map] or [S]kirmish or [M]uster:")

        while option.lower() == "map":
            self.do_map()
            option = raw_input("Enter choice: [map] or [S]kirmish or [M]uster:")

        print ""
        if option.lower() == "s":
            self.french_skirmish()
        else:
            self.french_muster()

    def french_battle(self):
        print ""
        print "BATTLE"
        print "Select Special Activity"

        self.french_skirmish_loop = True

        option = raw_input("Enter choice: [S]kirmish or [P]reparer la Guerre or [N]aval Pressure:")

        if option.lower() == "s":
            self.french_skirmish()
        elif option.lower() == "p":
            self.preparer_la_guerre()
        else:
            self.french_naval_pressure_loop = True
            self.french_naval_pressure()

        print ""
        print "ACTION: Manually resolve all Battles."
        print "Update using 'map' for all movements manually"

        option = raw_input("Enter choice: [map] or if none then [M]arch:")

        while option.lower() == "map":
            self.do_map(self)
            option = raw_input("Enter choice: [map] or [E]nd Battle section:")

        if option.lower() == "m":
            self.french_march()

    def do_patriot_flow(self, rest):

        if self.patriot_resources == 0:  # Patriots can't play event and no resources
            print "Patriots PASS as resources = 0"
            print "ACTION: Move Patriots into PASS Box"

        else:
            # print "[8.5.1] Checking for Rebel Cubes + Leader > Active Royalist pieces in space with both"

            # for country in self.map:
            #    rebellion_control = int(self.map[country].patriot_continental) + int(self.map[country].patriot_militia) + int(self.map[country].patriot_fort)
            #    if self.map[country].patriot_washington == True:
            #        rebellion_control += 1
                    # TO DO - also check for French leaders
            print "NOT IMPLEMENTED YET"


def main():
    print "GMT: Liberty or Death"
    print ""
    print "Release", RELEASE
    scenario = 0

    while 0 == scenario:
        try:
            print ""
            print "Choose Scenario (currently always '2')"
            print "(1) TBC"
            print "(2) British Return to New York; Duration: Medium; Time Range: 1776 to 1779"
            print "(3) TBC"
            input = raw_input("Enter choice: ")
            input = int(input)
            input = 2
            if 1 <= input <= 3:
                scenario = input
                print ""
            else:
                raise
        except:
            print "Scenario Selection error"
            print ""

    app = LoD(scenario)

    app.cmdloop()

if __name__ == "__main__":
    main()
