"""
    This file is part of tococyn.

    tococyn is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""

from enum import Enum, unique
from typing import Optional

from concepts import roll
from concepts.roll import Roll


@unique
class Era(Enum):
    """
    COC ERA
    """
    NineteenTwenty = 1
    Modern = 2
    Pulp = 3


class Attribute:
    """
    Value
    """

    def __init__(self, description: str, code: str, regular: int = None):
        self.description = description
        self.code = code
        self._regular = regular
        self._half = regular // 2
        self._fifth = regular // 5

    def __repr__(self):
        return f'{self.description}{"" if self.code is None else f"/{self.code}"}({"Not yet set" if self.regular is None else f"R: {self._regular} H:{self._half} F: {self._fifth}"})'

    @property
    def regular(self) -> int:
        """
        Get regular value
        :return: regular value
        """
        return self._regular

    @regular.setter
    def regular(self, regular: int):
        self._regular = regular
        self._half = regular // 2
        self._fifth = regular // 5

    @staticmethod
    def _compare(value: int, limit: Optional[int]) -> bool:
        """
        Verify if a value is lower than a limit. If no value is provided a random(100) will be generated
        :param value:  Value or None. In case of None a random value wil lbe generated.
        :param limit: Upper limmit
        :return: True if value is less than or equal to limit.
        """
        if value is None:
            value = roll.random_func(100)
        return value <= limit

    def is_regular(self, value: Optional[int]) -> bool:
        """
        Perform a regular check
        :param value: Value to check, if no value is provided a random(100) will be generated
        :return: True if value is less than or equal to _regular
        """
        return self._compare(value, self._regular)

    def is_hard(self, value: Optional[int]) -> bool:
        """
        Perform a hard check
        :param value: Value to check, if no value is provided a random(100) will be generated
        :return: True if value is less than or equal to _half
        """
        return self._compare(value, self._half)

    def is_extreme(self, value: Optional[int]):
        """
        Perform an extreme hard check
        :param value: Value to check, if no value is provided a random(100) will be generated
        :return: True if value is less than or equal to _fifth
        """
        return self._compare(value, self._fifth)

STR = "STR"
CON = "CON"
DEX = "DEX"
SIZ = "SIZ"
APP = "APP"
INT = "INT"
POW = "POW"
EDU = "EDU"


@unique
class Gender(Enum):
    """
    Sex
    """
    MALE = 1
    FEMALE = 2
    X = 3


    def person(self):
        if self == Gender.FEMALE:
            return "woman"
        elif self == Gender.MALE:
            return "man"
        return "X"



POSSESSIVE_PRONOUN = {
    Gender.MALE : "his",
    Gender.FEMALE : "her",
    Gender.X : "theirs"
}


OBJECT_PRONOUN = {
    Gender.MALE : "him",
    Gender.FEMALE : "her",
    Gender.X : "them"
}


PERSONAL_PRONOUN = {
    Gender.MALE : "he",
    Gender.FEMALE : "she",
    Gender.X : "they"
}


class Characteristic(Attribute):
    """
    Investigator characteristic
    """

    def __init__(self, code, description, regular):
        Attribute.__init__(self, code, description, regular)


class Investigator:
    """
    COC investigator
    """

    def __init__(self, firstname: str, surname: str, gender: Gender, occupation: str, birthplace: str, residence:str,age: int):
        self.firstname = firstname
        self.surname = surname
        self.gender = gender
        self.age = age
        self.possessive_p = POSSESSIVE_PRONOUN[gender]
        self.object_p = OBJECT_PRONOUN[gender]
        self.personal_p = PERSONAL_PRONOUN[gender]
        self.occupation = occupation
        self.birthplace = birthplace
        self.residence = residence
        self.strength = None
        self.constitution = None
        self.dexterity = None
        self.intelligence = None
        self.size = None
        self.power = None
        self.appearance = None
        self.education = None

    def __repr__(self):

        ret = f"{self.firstname} {self.surname} is a {self.age} year old {self.gender.person()} born in {self.birthplace} and living in {self.residence}. At the moment {self.gender.}"
        return ret

    @staticmethod
    def value_or_roll(description, key, **kwargs):
        ret = kwargs.get(key)
        if ret is None:
            ret = Roll(description).roll()
        return ret

    def generate_name(self, gender:Gender = None ) -> (str, str, Gender):
        """
        Generate a random
        :param gender:
        :return:
        """
        raise NotImplementedError()

    def set_characteristic(self, **kwargs):
        """

        :param kwargs:
        """
        self.strength = 5 * self.value_or_roll("3D6", STR, **kwargs)
        self.constitution = 5 * self.value_or_roll("3D6", CON, **kwargs)
        self.dexterity = 5 * self.value_or_roll("3D6", DEX, **kwargs)
        self.appearance = 5 * self.value_or_roll("3D6", APP, **kwargs)
        self.intelligence = 5 * self.value_or_roll("2D6+6", INT, **kwargs)
        self.size = 5 * self.value_or_roll("2D6+6", SIZ, **kwargs)


me = Investigator(firstname="Jessy",
                  surname="Williams",
                  gender=Gender.FEMALE,
                  birthplace="Boston",
                  residence="Arkham",
                  occupation=None,
                  age=20)


me.set_characteristic()
print(me.gender.person())

print(me)




#
# class Being:
#     """
#     CoC Investigator
#     """
#     def __init__(self, name, HP, era, **kwargs):
#         self.name = name
#         self.maxHP = self.HP = HP
#         self.era = era
#         self.db = 0
#         self.build = 0
#         self.mov = 8
#         self.luck = 0
#         self.san = self.maxSan = 0
#         self.mp = 0
#         self.numAttacks = 1
#         self.armor = 0
#         self.currentWeapon = None
#
#         self.status = dict()
#         self.status['fightback'] = True
#         self.characteristics = dict()
#         self.skills = dict()
#         self.weapons = dict()
#
#     def setCharacteristic(self, characteristic, value):
#         self.characteristics[characteristic] = skill(characteristic, value)
#
#     def setSkill(self, skillName, value):
#         self.skills[skillName] = skill(skillName, value)
#
#     def addWeapon(self, weaponName, skillName, damage, weaponType='non-impaling', db=False, mal=101, ammo=0, numAttacks=1):
#         if weaponType != 'firearm':
#             self.weapons[weaponName] = weapon(weaponName, skillName, damage, weaponType=weaponType,  db=db, mal=mal)
#         else:
#             self.weapons[weaponName] = firearm(weaponName, skillName, damage, weaponType=weaponType,  db=db, mal=mal, ammo=ammo, numAttacks=numAttacks)
#
#     def setDodge(self, value=0):
#         try:
#             self.skills['Dodge'] = skill('Dodge' , self.characteristics['DEX'].half)
#         except:
#             log.error("ERROR: Unable to set Dodge.")
#
#     def outNumbered(self):
#         """ returns True if they have already responded """
#         try:
#             if self.status['combat_response'] > self.numAttacks:
#                 return True
#         except KeyError:
#             self.status['combat_response'] = 0
#             return False
#
#         return False
#
#     def jsondump(self):
#         return jsonpickle.encode(self)
#
#     def initiative_value(self):
#         """ Return the initiative value for this character based on their current weapon. """
#         if self.currentWeapon is not None and self.currentWeapon.weaponType == 'firearm':
#             init_value = self.characteristics['DEX'].value + 50
#         else:
#             init_value = self.characteristics['DEX'].value
#
#         logging.debug("Combat: {} init value is {}".format(self.name, init_value))
#
#         return init_value
#
#     def setCurrentWeapon(self):
#         """ Ask the user what their current weapon should be. """
#         chosen = False
#         wlist = list(self.weapons)
#         if len(wlist) == 1:
#             weapon = 0
#             chosen = True
#
#         while chosen is False:
#
#             for w in wlist:
#                 print '{}. {} {}'.format(wlist.index(w)+1, w, self.weapons[w].damage)
#             weapon = raw_input('\n{} must choose their weapon: '.format(self.name))
#
#             try:
#                 weapon = int(weapon)-1
#                 if 0 <= weapon <= len(wlist)-1:
#                     chosen = True
#             except:
#                 pass
#
#         self.currentWeapon = self.weapons[wlist[weapon]]
#
# class Investigator(Being):
#     """
#     COC Investigator
#     """
#     def __init__(self, name=''):
#         Being.__init__(self, name)
#         for characteristic in ['STR', 'DEX', 'APP', 'CON', 'POW', 'INT', 'SIZ', 'EDU']:
#             self.setCharacteristic(characteristic, 0)
#
#         # only characters should check for major wounds. Is this true? Need to verify.
#         self.majorWound = 0
#
#         self.addWeapon('Unarmed',  '1d3', 'Fighting (Brawl)', db=True)  # ADD DAMAGE BONUS
#
#     def setSecondary(self):
#         self.setHP()
#         self.setSAN()
#         self.setBuildAndDB()
#         self.setMOV()
#         self.setMP()
#         self.setDodge()
#
#     def setHP(self):
#         """ Sets the maximum HP and current HP based on CON and SIZ.
#              Modify self.HP directly if you need to subtract or add HP.
#         """
#         try:
#             self.maxHP = (self.characteristics['CON'].value + self.characteristics['SIZ'].value) / 10
#             self.HP = self.maxHP
#         except:
#             logging.error("ERROR: Missing CON or SIZ. Please add those before setting HP.")
#
#     def setBuildAndDB(self):
#         """ Sets the initial damage bonus and build based on STR and SIZ. """
#         try:
#             combined = self.characteristics['STR'].value + self.characteristics['SIZ'].value
#         except:
#             logging.error("ERROR: Missing STR or SIZ. Please add before setting up DB and build.")
#             return
#
#         if 2 <= combined <= 64:
#             self.db = self.build = -2
#         elif 65 <= combined <= 84:
#             self.db = self.build = -1
#         elif 125 <= combined <= 164:
#             self.db = '1d4'
#             self.build = 1
#         elif combined >= 165:
#             self.db = '1d6'
#             self.build = 2
#
#     def setMOV(self):
#         """ Sets MOV based on DEX, STR and SIZ. """
#         try:
#             if self.characteristics['STR'].value < self.characteristics['SIZ'].value and \
#                self.characteristics['DEX'].value < self.characteristics['SIZ'].value:
#                    self.mov = 7
#             elif self.characteristics['STR'].value > self.characteristics['SIZ'].value and \
#                    self.characteristics['DEX'].value > self.characteristics['SIZ'].value:
#                    self.mov = 9
#         except:
#             logging.error('ERROR: Cannot set MOV. Missing STR, DEX or SIZ.')
#
#     def setSAN(self):
#         """ Sets the initial sanity. """
#         try:
#             self.san = self.characteristics['POW'].value
#             self.maxSan = self.san
#         except:
#             logging.error('ERROR: Need POW before we can set SAN.')
#
#     def setMP(self):
#         """ Sets the inital POW."""
#         try:
#             self.mp = self.characteristics['POW'].fifth
#         except:
#             logging.error('ERROR: Need POW before we can set MP.')
#
#     def checkMajorWound(self, damage):
#         # check for major wound
#         if self.HP > 0 and damage >= (self.maxHP / 2):
#             logging.info('DAMAGE: {} suffered a major wound.'.format(self.name))
#             # make a CON check
#             if self.characteristics['CON'].check() < result.normal:
#                 logging.info('DAMAGE: {} failed their CON check - falling unconscious and will die.'.format(self.name))
#                 self.HP = 0
#
#
#     def __str__(self):
#         outstr = "Name: {}\n".format(self.name)
#         outstr = outstr + "Era: {}\n".format(self.era)
#         outstr = outstr +  "HP: {}\tMax HP: {}\tMP: {}\n".format(self.HP, self.maxHP, self.mp)
#         outstr = outstr +  "San: {}\tMax SAN: {}\n".format(self.san, self.maxSan)
#         outstr = outstr +  'DB: {}\tBuild: {}\tMOV: {}\n'.format(self.db, self.build, self.mov)
#         outstr = outstr +  'Luck: {}\n\n'.format(self.luck)
#         outstr = outstr +  "Characteristics:\n"
#         for characteristic in self.characteristics:
#             outstr = outstr +  str(self.characteristics[characteristic]) + '\n'
#
#         outstr = outstr + "\nSkills:\n"
#         for skills in sorted(self.skills):
#             outstr = outstr +  str(self.skills[skills]) + '\n'
#
#         outstr = outstr + "\nWeapons:\n"
#         for weapon in sorted(self.weapons):
#             outstr = outstr +  str(self.weapons[weapon]) + '\n'
#
#         return outstr
#
# class monster(being):
#     def __init__(self, name=''):
#         being.__init__(self, name)
#         for characteristic in ['STR', 'DEX', 'APP', 'CON', 'POW', 'INT', 'SIZ', 'EDU']:
#             self.setCharacteristic(characteristic, 0)
#
#         self.sanLoss = '0/0'
#         self.majorWound = 0
#
#     def __str__(self):
#         outstr = "Name: {}\n".format(self.name)
#         outstr = outstr +  "HP: {}\tMax HP: {}\tMP: {}\n".format(self.HP, self.maxHP, self.mp)
#         outstr = outstr +  'DB: {}\tBuild: {}\tMOV: {}\n'.format(self.db, self.build, self.mov)
#         outstr = outstr + 'Armor: {}\tNumber of Attacks: {}\tSanity Loss: {}\n\n'.format(self.armor, self.numAttacks, self.sanLoss)
#         outstr = outstr +  "Characteristics:\n"
#         for characteristic in self.characteristics:
#             if self.characteristics[characteristic].value > 0:
#                 outstr = outstr +  str(self.characteristics[characteristic]) + '\n'
#
#         outstr = outstr + "\nSkills:\n"
#         for skills in sorted(self.skills):
#             outstr = outstr +  str(self.skills[skills]) + '\n'
#
#         outstr = outstr + "\nWeapons:\n"
#         for weapon in sorted(self.weapons):
#             outstr = outstr +  str(self.weapons[weapon]) + '\n'
#         return outstr
#
# def json_import(myjson):
#     """ Imports the char.jsondump() version of a char and returns the new object. """
#     return jsonpickle.decode(myjson)
#
# if __name__ == "__name__":
#     raise NotImplementedError()
