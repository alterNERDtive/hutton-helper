"""
Broadcasts to the Hutton Helper web site.
"""

from version import HH_VERSION

import json
import zlib

import plugin
import xmit

ADDITIONAL_PATHS_URL = 'http://hot.forthemug.com/event_paths.json'

class ForTheMugPlugin(plugin.HuttonHelperPlugin):
    "Forwards data to the Hutton Helper Server."

    event_paths = {
      "Bounty": "/bounty",
      "Cargo": "/cargo",
      "CargoDepot": "/cargodepot",
      "CollectCargo": "/cargocollection",
      "CommitCrime": "/commitcrime",
      "CommunityGoal": "/communitygoal",
      "Died": "/death",
      "Docked": "/dockedinfoupdate",
      "EjectCargo": "/ejectcargo",
      "EscapeInterdiction" : "/escapeinterdiction",
      "FactionKillBond": "/factionkillbond",
      "Friends" : "/friends",
      "FSDJump": "/fsdjump",
      "FSSSignalDiscovered": "/fsssignaldiscovered",
      "Interdicted" : "/interdicted",
      "Interdiction" : "/interdiction",
      "LoadGame": "/loadgame",
      "Loadout": "/loadout",
      "MarketBuy": "/buy",
      "MarketSell": "/sell",
      "MiningRefined": "/miningrefined",
      "MissionAbandoned": "/missioncomplete",
      "MissionAccepted": "/missiontake",
      "MissionCompleted": "/missioncomplete",
      "MissionFailed": "/missioncomplete",
      "MissionRedirected": "/missionupdate",
      "MultiSellExplorationData": "/multisellexplorationdata",
      "NpcCrewPaidWage": "/npccrewpaidwage",
      "Promotion": "/cmdrpromotion",
      "ProspectedAsteroid": "/prospectedasteroid",
      "Rank": "/rank",
      "ReceiveText": "/receivetext",
      "SAAScanComplete": "/saascancomplete",
      "SAASignalsFound": "/saasignalsfound",
      "Scan": "/scan",
      "SellExplorationData": "/explorationdata",
      "SquadronStartup": "/squadronstartup",
      "StartJump": "/startjump",
      "Statistics": "/stats",
      "SupercruiseEntry": "/supercruiseentry",
      "SupercruiseExit": "/supercruiseexit",
      "Undocked": "/undockedinfoupdate",
      "USSDrop" : "/ussdrop"
    }


    def plugin_start(self):
        "Called once at startup. Try to keep it short..."
        extra_paths = xmit.get(ADDITIONAL_PATHS_URL)

        if extra_paths is not None:
            self.event_paths = extra_paths



    def journal_entry(self, cmdr, is_beta, system, station, entry, state):
        "Called when Elite Dangerous writes to the commander's journal."

        event = entry['event']
        event_path = self.event_paths.get(event)

        compress_json = json.dumps(entry)
        transmit_json = zlib.compress(compress_json)

        if event_path:
            xmit.post(event_path, data=transmit_json, parse=False, headers=xmit.COMPRESSED_OCTET_STREAM)
