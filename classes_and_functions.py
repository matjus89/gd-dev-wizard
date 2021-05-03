from statistics import mean

unlocked_stars = []  # Stores every star that has been unlocked.


class SpecificDevotionPoints:
    """
    The class represents the in-game affinity.
    """
    def __init__(self, name, points=0, crossroads_lock=True, minimum=0):
        """

        :param name: The name of an affinity.
        :param points: Defines a current number of points accumulated to a specific affinity.
        :param crossroads_lock:
        :param minimum: Defines the minimum number of points needed for all unlocked stars to stay in unlocked status.
        """
        self.name = name
        self.points = points
        self.crossroads_lock = crossroads_lock
        self.minimum = minimum

    def __repr__(self):
        return "{} : {}".format(self.name, self.points)

    def add_points(self, x):
        """
        Upon unlocking the last star of a constellation a bonus of affinity points is added to affinity points pool.
        :param x: The number of points added.
        :return:
        """

        self.points += x
        return self.points

    def deduct_points(self, point):
        self.points -= point
        return self.points

    def set_minimum(self, requirement):
        """
        Set a border below which affinity points cannot go.
        :return: a minimum number of points needed to keep all stars in unlocked state.
        """

        if requirement > self.minimum:
            self.minimum = requirement
        return self.minimum

    def reset_minimum(self):
        """
        Set the minimum number of required points to zero.
        :return: The minimum number of devotion points.
        """
        self.minimum = 0
        return self.minimum

    def zero(self):
        """
        Resets affinity points to the default number.
        :return: Default number of affinity points(0).
        """
        if self.points > 0:
            self.points = self.points - self.points
        return self.points


class Ascendants(SpecificDevotionPoints):
    def __init__(self, name):
        self.name = name
        SpecificDevotionPoints.__init__(self, name)


class Primordial(SpecificDevotionPoints):
    def __init__(self, name):
        self.name = name
        SpecificDevotionPoints.__init__(self, name)


class Eldritch(SpecificDevotionPoints):
    def __init__(self, name):
        self.name = name
        SpecificDevotionPoints.__init__(self, name)


class Order(SpecificDevotionPoints):
    def __init__(self, name):
        self.name = name
        SpecificDevotionPoints.__init__(self, name)


class Chaos(SpecificDevotionPoints):
    def __init__(self, name):
        self.name = name
        SpecificDevotionPoints.__init__(self, name)


Points_of_Ascendant = Ascendants('Points_of_Ascendant')
Points_of_Order = Order('Points_of_Order')
Points_of_Eldritch = Eldritch('Points_of_Eldritch')
Points_of_Primordial = Primordial('Points_of_Primordial')
Points_of_Chaos = Chaos('Points_of_Chaos')
affinities = [Points_of_Ascendant, Points_of_Order, Points_of_Eldritch, Points_of_Primordial, Points_of_Chaos]


class DevotionPointsPool:
    """
    The class represents the in-game devotion points.
    """
    def __init__(self, devpoints):
        """
        :param devpoints: The number of devotion points.
        """
        self.devpoints = devpoints

    def __repr__(self):
        return "Devotion points available: {}".format(self.devpoints)

    def deduct_point(self):
        """
        Deduct devotion point when unlocking a star.
        :return: Updated devotion points number.
        """
        self.devpoints = self.devpoints - 1
        return self.devpoints

    def add(self):
        """
        Add a point if a star is locked.
        :return: Updated devotion points number.
        """
        self.devpoints = self.devpoints + 1
        return self.devpoints

    def reset(self):
        """
        Resets the number of devotion points to the default number.
        :return: The default, starting number of devotion points.
        """
        self.devpoints = 55
        return self.devpoints


Devotion_Points_Pool = DevotionPointsPool(55)


class Star:
    """
    The class represents the in-game star.
    """
    def __init__(self, source, name=None, unlockr=None, bonus_type=None, bonus_value=None, requirement_type=None,
                 affinity=False, tier=1, line=None, **kwargs):
        """
        :param source: The source name. It is shared along all stars of a particular constellation, e.g. Panther
        :param name: A unique name for a star, created based on its position in a constellation, e.g. First Panther Star
        :param unlockr: Number of affinity points required to unlock a star.
        :param bonus_type: Affinity type points gained upon unlocking all stars of a constellation.
        :param bonus_value: Number of affinity points gained upon unlocking all stars of a constellation.
        The index of this number corresponds to the index of affinity type in bonus_type list.
        :param requirement_type: Affinity type points required to unlock the first star of a constellation.
        The index of this number corresponds to the index of affinity type in requirement_type list.
        :param affinity: This indicates that once the star(self) is unlocked the program should check if it is possible
        to add affinity bonus to the respective affinity pool.
        :param tier: Defines how many stars of a constellation have to be unlocked before this star(self) can be
        unlocked.
        :param line: The line can be undefined which means that the star can be unlocked without checking any
        additional requirements beyond self.tier. Otherwise it can be assigned a number value. Each new line number
        reflects a fork in a constellation structure. A star with a number as self.line value must take into account
        other stars with the same self.line during the unlocking process.
        :param kwargs: key word arguments represent in-game attributes.
        """
        self.source = source
        self.name = name
        self.unlockr = unlockr
        self.bonus_type = bonus_type
        self.bonus_value = bonus_value
        self.requirement_type = requirement_type
        self.__dict__.update(**kwargs)
        self.affinity = affinity
        self.tier = tier
        self.line = line

    def __repr__(self):
        return '{}'.format(self.name)

    def permit_locking(self):
        """
        Check if a star can be locked. Locking of a star cannot break the in-game mechanics.
        :return: True if a star can be locked.
        """

        lock_permission = True
        const = self.find_constellation()
        members_unlocked = [x for x in const.members if x in unlocked_stars]
        members_lines = [x.line for x in members_unlocked]
        lines = None
        ranks_list = [x.rank for x in unlocked_stars if x.source == self.source]
        # The main line star has to follow the normal rank locking/unlocking mechanics.
        if self.line is None:
            for i in ranks_list:
                if i > self.rank:
                    lock_permission = False
                    break
                else:
                    lock_permission = True
            return lock_permission
        # If self.line is an integer, check if there are other unlocked stars of the same constellation which share the
        # same line integer. If not, the program can disregard the star rank and grant permission.
        elif self.line and members_lines.count(self.line) == 1:
            return lock_permission
        # If there is more stars with the same line value, the program has to check rank values.
        elif self.line and members_lines.count(self.line) > 1:
            lines = [x for x in members_unlocked if x.line == self.line and x != self]
        for i in lines:
            if i.rank > self.rank:
                lock_permission = False
                return lock_permission
            elif i.rank <= self.rank:
                lock_permission = True
        return lock_permission

    def add_bonus(self):
        """
        Add bonus attributes to the attributes dictionary. This process ensures that later on all results(summed up
        values of attributes) can be send out to the frontend and displayed when 'results' button is clicked.
        :return: Updated attributes dictionary.
        """
        if self in unlocked_stars:
            for i in self.__dict__:
                # Ensure that only attributes referring to the in-game bonuses are added to the dictionary. This avoids
                # adding instance attributes like rank, line or bonus_type.
                if i in attributes_dict:
                    if type(self.__dict__[i]) == list:
                        attributes_dict[i].extend(self.__dict__[i])
                    else:
                        attributes_dict[i].append(self.__dict__[i])
        return attributes_dict

    def unlock(self):
        """
        Unlocks a star provided that it has not been already unlocked.
        :return: The list of unlocked stars.
        """
        if Devotion_Points_Pool.devpoints > 0 and self.name not in unlocked_stars:
            unlocked_stars.append(self)
            Devotion_Points_Pool.deduct_point()
        return unlocked_stars

    def check_requirement(self, only_info=False):
        """
        Check if a star meets all affinity, devotion points, lines and ranks requirements.
        :param only_info: Used in glow_stars() function. If true, the program will only transfer an information that a
        star can be unlocked or not without actual unlocking.
        :return: A list of unlocked stars if only info_is false, otherwise a list of stars that could be unlocked.
        """
        const = self.find_constellation()
        members_unlocked = [c for c in unlocked_stars if c in const.members]
        to_glow = []
        # if this is the first star in a constellation structure.
        if self.rank == 0 and self.requirement_type != 0 and self not in unlocked_stars:
            # if there is one affinity requirement for the given star.
            if len(self.unlockr) == 1:
                # if there is enough affinity points to unlock a given star
                if self.unlockr[0] <= self.requirement_type[0].points:
                    if only_info:
                        to_glow.append(self)
                    else:
                        self.unlock()
                        self.add_bonus()
                        self.requirement_type[0].set_minimum(self.unlockr[0])
            # if there is two affinity requirements for the given star.
            if len(self.unlockr) == 2:
                if self.unlockr[1] <= self.requirement_type[1].points and self.unlockr[0] <= \
                        self.requirement_type[0].points:
                    if only_info:
                        to_glow.append(self)
                    else:
                        self.unlock()
                        self.add_bonus()
            # if there is three affinity requirements for the given star.
            if len(self.unlockr) == 3:
                if self.unlockr[2] <= self.requirement_type[2].points and self.unlockr[1] <= \
                        self.requirement_type[1].points and self.unlockr[0] <= self.requirement_type[0].points:
                    if only_info:
                        to_glow.append(self)
                    else:
                        self.unlock()
                        self.add_bonus()
        # unlocking any other star
        else:
            if self.line is None and self.rank <= len(members_unlocked):
                if only_info:
                    to_glow.append(self)
                else:
                    self.unlock()
                    self.add_bonus()
                    self.affinity_bonus(const, len(const.members[0].bonus_type))
            elif self.line:
                line_matches = [x for x in members_unlocked if x.line is None or x.line == self.line]
                if self.rank <= len(line_matches):
                    if only_info:
                        to_glow.append(self)
                    else:
                        self.unlock()
                        self.add_bonus()
                        self.affinity_bonus(const, len(const.members[0].bonus_type))
        if only_info:
            return to_glow
        else:
            return unlocked_stars

    def affinity_bonus(self, const, aff_number):
        """
        Adds points to the affinities defined in the first star of a constellation.
        :param const: Constellation to check.
        :param aff_number: Number of required affinity types of a constellation.
        :return: True if affinity bonus was succesfully added.
        """
        if 'Crossroads' in self.name and self not in unlocked_stars:
            const.members[0].bonus_type[0].add_points(const.members[0].bonus_value[0])
        # Confirm that all stars of a constellation has been unlocked and that the constellation grants some bonus
        # to affinities.
        elif const.check_full() and const.affinity_bonus:
            for i in range(0, aff_number):
                const.members[0].bonus_type[i].add_points(const.members[0].bonus_value[i])
        return True

    def display_attr(self):
        """
        Arrange the star's attributes into the string format known from the game. The returned list of strings
        is sent to frontend and set into paragraphs.
        :return: A list of strings made from stars objects' attributes.
        """
        # Ensure that only stars granting skills have its self.name displayed. Display source name for the rest.
        if self.find_constellation().members[-1] == self and 'Third' not in self.name and 'Fourth' not in self.name \
                and 'Fifth' not in self.name and 'Sixth' not in self.name:
            name_to_display = self.name
        else:
            name_to_display = self.source.replace('_', ' ')
        attributes = [x for x in self.__dict__ if x in attributes_dict]
        result = []
        replaced = None
        unwanted = None
        replaced_two = None
        unwanted_two = None
        specific_done = False

        for i in attributes:
            # The below block of code arranges the attributes of skills which involve summoning pets into strings which
            # then will be sent to the app frontend.
            if type(self.__dict__[i]) == dict:
                # The dictionary as a star attribute means that its stored values refer to the in-game pet bonuses or
                # special skills.
                pet_list = list(self.__dict__[i].values())
                result.extend(pet_list)
                # Strings 'specific' and 'particular' will enable frontend code to put the attributes into
                # the right order.
                if 'Attributes' not in i and 'Abilities' not in i and specific_done is False:
                    result.append(i + ' specific')
                    specific_done = True
                elif 'Attributes' not in i and 'Abilities' not in i and specific_done:
                    result.append(i + ' particular')
                else:
                    result.append(i)
            # Some rare bonuses required hard coding to reflect the in-game display. These are usually attributes with
            # two values.
            elif type(self.__dict__[i]) != list:
                if 'Knockdown' in i:
                    if self == trample:
                        result.append('Knockdown target for 0.8 - 1.5 Seconds'.format(a=str(self.__dict__[i])))
                    else:
                        result.append('Knockdown target for {a} Seconds'.format(a=str(self.__dict__[i])))
                elif 'Chance_to_Stun' in i:
                    result.append('Stun target for {a} Seconds'.format(a=self.__dict__[i]))
                elif 'Chance_to_Confuse' in i:
                    result.append('Confuse target for {a} Seconds'.format(a=self.__dict__[i]))
                elif 'Lives' in i:
                    result.append('Lives for {a} Seconds'.format(a=str(self.__dict__[i])))
                elif 'Energy_Leech_Chance' in i:
                    result.append('Chance for {a} Energy Leech'.format(a=str(self.__dict__[i])))
                elif 'Invincible' in i:
                    result.append('Invincible')
                elif self == hungering_void and '308 Active Health Cost per Second' not in result:
                    result.append('308 Active Health Cost per Second')
                elif 'Chance_to_Petrify' in i:
                    result.append('Petrify target for {a} Seconds'.format(a=self.__dict__[i]))
                elif 'Affected_Targets' in i:
                    result.append('Affects up to {a} targets'.format(a=self.__dict__[i]))
                # Value as a float requires special treatment as well. Some must be displayed as '%', some as float.
                elif type(self.__dict__[i]) == float and 'per' not in i and 'Seconds_Skill_Recharge' not in i and \
                        'Radius' not in i and 'Area' not in i and 'Knockdown' not in i and 'Lives' not in i and 'Stun' \
                        not in i and 'Confuse' not in i and 'Petrify' not in i and 'Affected' not in i:
                    self.__dict__[i] = "{:.0%}".format(self.__dict__[i])
                else:
                    if 'Duration' in i and 'Reduced' in i and 'Knockdown' not in i and type(self.__dict__[i]) != str:
                        self.__dict__[i] = "{:.0%}".format(self.__dict__[i])
                        result.append(str(self.__dict__[i]) + ' ' + i)
                    elif 'Knockdown' not in i and 'Stun' not in i and 'Confuse' not in i and 'Affected' not in i:
                        result.append(str(self.__dict__[i]) + ' ' + i)
            # The list occurs when there are two values but the display is not meant for a pet bonus nor skill.
            elif type(self.__dict__[i]) == list:
                if 'Chance_to_Stun' in i:
                    a = "{:.0%}".format(self.__dict__[i][0])
                    if self == hungering_void:
                        result.append('pets {a} Chance to Stun target for {b} Seconds'.
                                      format(a=a, b=self.__dict__[i][1]))
                    else:
                        result.append('{a} Chance to Stun target for {b} Seconds'.format(a=a, b=self.__dict__[i][1]))
                elif 'Chance_to_Confuse' in i:
                    a = "{:.0%}".format(self.__dict__[i][0])
                    result.append('{a} Chance to Confuse target for {b} Seconds'.format(a=a, b=self.__dict__[i][1]))
                elif 'Restored' in i:
                    a = "{:.0%}".format(self.__dict__[i][0])
                    result.append('{a} + {b} Health Restored'.format(a=a, b=self.__dict__[i][1]))
                elif 'Restored' in i:
                    a = "{:.0%}".format(self.__dict__[i][0])
                    result.append('{a} + {b} Health Restored'.format(a=a, b=self.__dict__[i][1]))
                elif 'Chance_to_Petrify' in i:
                    a = "{:.0%}".format(self.__dict__[i][0])
                    result.append('{a} Chance to Petrify target for {b} Seconds'.format(a=a, b=self.__dict__[i][1]))
                elif 'Slow_Target' in i:
                    if len(self.__dict__[i]) == 3:
                        a = "{:.0%}".format(self.__dict__[i][0])
                        b = "{:.0%}".format(self.__dict__[i][1])
                        result.append('pets {a} Chance of {b} slow target for {c} Seconds'.
                                      format(a=a, b=b, c=self.__dict__[i][2]))
                    else:
                        a = "{:.0%}".format(self.__dict__[i][0])
                        result.append('{a} Slow target for {b} Seconds'.format(a=a, b=self.__dict__[i][1]))
                else:
                    if type(self.__dict__[i][1]) == float and 'per' not in i and 'Seconds_Skill_Recharge' not in i and \
                            'Radius' not in i:
                        second_string = "{:.0%}".format(self.__dict__[i][1]) + ' ' + i
                        result.append(second_string)
                    if type(self.__dict__[i][1]) != float:
                        second_string = str(self.__dict__[i][1]) + ' ' + i
                        result.append(second_string)
                    if type(self.__dict__[i][0]) == float and 'per' not in i and 'Seconds_Skill_Recharge' not in i and \
                            'Radius' not in i:
                        first_string = "{:.0%}".format(self.__dict__[i][0]) + ' ' + i
                        result.append(first_string)
                    if type(self.__dict__[i][0]) != float:
                        first_string = str(self.__dict__[i][0]) + ' ' + i
                        result.append(first_string)
        result.append(name_to_display)
        # Turn python range object into 'number-number' format.
        for i in result:
            if 'range(' in i:
                if replaced:
                    unwanted_two = result.index(i)
                    replaced_two = i.replace("range(", "")
                else:
                    unwanted = result.index(i)
                    replaced = i.replace("range(", "")
        for i in result:
            if i in self.__dict__ and type(self.__dict__[i]) == float:
                self.__dict__[i] = "{:.1%}".format(self.__dict__[i])
                break
        if replaced:
            replaced = replaced.replace(',', ' -')
            replaced = replaced.replace(')', '')
            result[unwanted] = replaced
        if replaced_two:
            replaced_two = replaced_two.replace(',', ' -')
            replaced_two = replaced_two.replace(')', '')
            result[unwanted_two] = replaced_two
        # Get rid of the underscore character required to create a class attribute.
        for i in result:
            if '_' in i:
                result[result.index(i)] = i.replace('_', ' ')
        for i in result:
            if 'target' in i and 'Petrify' not in i and 'Knockdown' not in i and 'Stun' not in i and 'Slow' not in i \
                    and 'Affects' not in i:
                result[result.index(i)] = i.replace('target', "target's")
        for i in result:
            if 'True pets Taunt Target' in i:
                result[result.index(i)] = i.replace('True pets Taunt Target', "pets Taunt target")
            if 'of 250' in i:
                result[result.index(i)] = i.replace('of 250', "of 250%")
        return result

    def lock(self, aff_number):
        """
        Lock a star and remove any bonuses assigned to it.
        :param aff_number: The number of affinity types required to unlock a star.
        :return: The list of unlocked stars.
        """

        const = self.find_constellation()
        counter = 0
        if 'Crossroads' in self.name and self in unlocked_stars:
            if self.bonus_type[0].minimum <= self.bonus_type[0].points - self.bonus_value[0]:
                Devotion_Points_Pool.add()
                unlocked_stars.remove(self)
                const.reset_unlock_status()
                self.bonus_type[0].deduct_points(self.bonus_value[0])
        elif 'Crossroads' not in self.name and self in unlocked_stars and self.permit_locking():
            # Remove all bonuses, attributes and add a devotion point.
            for i in range(0, aff_number):
                full = const.check_full()
                # Remove affinity bonuses if all stars of a constellation have been unlocked.
                if full and const.affinity_bonus:
                    if const.members[0].bonus_type[i].minimum <= \
                            const.members[0].bonus_type[i].points - const.members[0].bonus_value[i]:
                        const.members[0].bonus_type[i].deduct_points(const.members[0].bonus_value[i])
                        counter += 1
                        if counter == aff_number:
                            Devotion_Points_Pool.add()
                            unlocked_stars.remove(self)
                            const.reset_unlock_status()
                            break
                # Do not deduct ay affinity points from its pool if all stars of a constellation have not been unlocked.
                else:
                    if const.members[0].requirement_type[i].minimum <= const.members[0].requirement_type[i].points:
                        Devotion_Points_Pool.add()
                        unlocked_stars.remove(self)
                        const.reset_unlock_status()
                        break
        # Remove bonuses to attributes which the star(self) used to grant before it'd got locked.
        for i in self.__dict__:
            if i in attributes_dict:
                if type(attributes_dict[i]) == list and self.__dict__[i] in attributes_dict[i]:
                    attributes_dict[i].remove(self.__dict__[i])
        return unlocked_stars

    def find_constellation(self):
        """
        Identify a star's constellation.
        :return: The star's constellation.
        """
        for constellation in constellations:
            if self.source == constellation.name:
                return constellation


# The dictionary stores all in-game attributes as keys and its gained values.
attributes_dict = {'Fragments': [], 'Meter_Range': [], 'Chance_for_Target_to_Fumble_Attacks': [],
                   'pets_Maximum_all_Resistances': [], 'Seconds_to_All_Currently_Active_Skills_Cooldowns': [],
                   'Black_Blood_of_Yugol_Attributes': [], 'Black_Blood': [], 'Skeleton_Attributes': [],
                   'Melee_Attack': [], 'Arcane_Mark': [], 'Arcane_Bomb_Attributes': [], 'Living_Shadow_Attributes': [],
                   'Shadow_Strike': [], 'Shadow_Blades': [], 'Arcane_Current_Attributes': [], 'Surge': [],
                   'Burning_Presence': [], 'Detonate': [], 'Elemental_Seeker_Attributes': [], 'Summon_Limit': [],
                   'Eldritch_Hound_Abilities': [], 'Tooth_and_Claws': [], 'Eldritch_Hound_Attributes': [],
                   'Affected_Targets': [], 'Chance_to_Confuse': [], 'Physical_Damage_Converted_to_Chaos_Damage': [],
                   'Knockdown': [], 'Chance_to_Stun': [], 'Meter_Target_Area': [], 'Health_Restored': [],
                   'Projectiles': [], 'Energy_Restored': [], 'Slow_Target': [], 'Burn_Retaliation': [],
                   'Seconds_Skill_Recharge': [], 'Meter_Radius': [], 'Second_Duration': [], 'Reduced_target_Damage': [],
                   'Reduced_target_Physical_Damage': [], 'of_Retaliation_Damage_added_to_Attack': [],
                   'Chance_to_Petrify_Target': [], 'pets_Taunt_Target': [], 'Damage_to_Undead': [],
                   'Reduced_target_Resistances': [],  'Reduction_in_Bleeding_Duration': [], 'pets_Poison_Damage': [],
                   'Chance_to_Freeze_Target': [], 'Reduction_in_Poison_Duration': [], 'Damage_Absorbtion': [],
                   'Reduced_target_Defensive_Ability': [], 'Damage_Absorption': [], 'Slower_target_Movement': [],
                   'Reduced_Freeze_Duration': [], 'Reduced_Stun_Duration': [], 'pets_to_All_Retaliation_Damage': [],
                   'pets_Defensive_Ability': [], 'pets_Offensive_Ability': [], 'pets_Crit_Damage': [],
                   'Reduced_target_Offensive_Ability': [], 'Chance_to_pass_through_Enemies': [], 'Energy_Leech': [],
                   'Physique_Requirement_for_Armor': [], 'Chance_of_250_Lightining_Damage': [],
                   'pets_Chance_of_Slow_Target': [], 'pets_Chance_to_Stun_Target': [], 'Terrify_Chance': [],
                   'Chaos_Retaliation_Damage': [], 'Invincible': [], 'Energy': [], 'Increases_Armor': [],
                   'Damage_to_Beasts': [], 'Reduced_Petrify_Duration': [], 'Slower_Enemy_Attack': [],
                   'pets_Reduced_Mind_Control_Seconds_Duration': [], 'pets_Physical_Resistance': [],
                   'Seconds_Duration': [], 'Fire_Resistance': [], 'Increases_Energy_Regeneration': [],
                   'Max_Bleeding_Resistance': [], 'pest_Bleeding_Damage': [], 'Damage_To_Beasts': [],
                   'Physique_Requirement_for_Melee_Weapons': [], 'Cunning_Requirement_for_Melee_Weapons': [],
                   'pets_Elemental_Damage': [], 'pets_Reduced_Seconds_Duration': [], 'pets_Reduced_Freeze_Duration': [],
                   'pets_Pierce_Resistance': [], 'pets_Lightining_Damage': [], 'Skill_Energy_Cost': [],
                   'Increases_Armor_Piercing': [], 'Spirit_Requirement_for_Weapon': [], 'Maximum_Fire_Resistance': [],
                   'Spirit_Requirement_for_Jewelry': [], 'Energy_Leech_Resistance': [], 'to_All_Damage': [],
                   'pets_Resistance_to_Life_Reduction': [], 'Reduction_in_Vitality_Decay_Seconds_Duration': [],
                   'Reduction_in_Electrocute_Seconds_Duration': [], 'Reduction_in_Frostbite_Seconds_Duration': [],
                   'Reduction_in_Burn_Seconds_Duration': [], 'Reduction_in_Poison_Seconds_Duration': [],
                   'Reduction_in_Bleeding_Seconds_Duration': [], 'Reduction_in_Internal_Trauma_Seconds_Duration': [],
                   'Chance_of_Lightining_Damage': [], 'Lightining_Retaliation': [], 'Less_Damage_From_Beasts': [],
                   'Reduced_target_Elemental_Resistances': [], 'Less_Damage_from_Undead': [], 'pets_Total_Speed': [],
                   'Maximum_Poison_and_Acid_Resistance': [], 'Skill_Disruption_Protection': [], 'Casting_Speed': [],
                   'Increases_Armor_Absorption': [], 'Physical_Damage_Retaliation': [],
                   'Maximum_Aether_Resistance': [], 'Maximum_Chaos_Resistance': [], 'pets_Bleeding_Resistance': [],
                   'Damage_to_Chthonics': [], 'pets_Resistance_To_Life_Reduction': [], 'pets_Physical_Damage': [],
                   'pets_Health_Regenerated_Per_Second': [], 'Elemental_Resistance': [],
                   'Cunning_Requirement_for_Ranged_Weapons': [], 'pets_Attack_Speed': [],  'Spirit_req_weapons': [],
                   'Physique_Requirement_For_Shields': [], 'pets_Health': [], 'piercing_increase': [],
                   'Elemental_Damage': [], 'Reduced_PetrifySeconds_Duration': [], 'pets_Chaos_Resistance': [],
                   'pets_Poison_and_Acid_Resistance': [],  'Maximum_Pierce_Resistance': [], 'Pierce_Damage': [],
                   'Shield_Block_Chance': [], 'Shield_Recovery': [], 'Pierce_Resistance': [], 'Damage_to_Humans': [],
                   'Shield_Damage_Blocked': [],  'Healing_Effects_Increased': [], 'Life_Leech_Resistance': [],
                   'reduced_Elemental_Resistanceistance': [], 'light_retal': [], 'Armor_increase': [],
                   'Fire_Retaliation': [], 'Maximum_Vitality_Resistance': [], 'Reduced_Entrapment_Duration': [],
                   'Reflected_Damage_Reduction': [], 'Vitality_Decay': [], 'Maximum_Lightining_Resistance': [],
                   'pets_Vitality_Resistance': [], 'pets_Aether_Resistance': [], 'pets_to_All_Damage': [],
                   'to_All_Retaliation_Damage': [], 'Health': [], 'Defensive_Ability': [], 'Physique_req': [],
                   'Physical_Damage': [], 'Cunning': [], 'Weapon_Damage': [], 'Chance_to_Avoid_Melee_Attacks': [],
                   'Chance_to_Avoid_Projectiles': [], 'Movement_Speed': [], 'Physique': [], 'Armor': [],
                   'Constitution': [], 'Internal_Trauma_Damage': [], 'Cold_Resistance': [], 'Attack_Speed': [],
                   'Lightining_Resistance': [], 'Poison_and_Acid_Resistance': [], 'Bleeding_Resistance': [],
                   'Vitality_Resistance': [], 'Chaos_Resistance': [], 'Aether_Resistance': [], 'Slow_Resistance': [],
                   'pets_Increases_Health_Regeneration': [], 'Spirit': [], 'Acid_Retaliation': [], 'Poison_Damage': [],
                   'Acid_Damage': [], 'Chaos_Damage': [], 'Aether_Damage': [], 'Vitality_Damage': [],
                   'Bleeding_Damage': [], 'Fire_Damage': [], 'Cold_Damage': [], 'Lightining_Damage': [],
                   'Burn_Damage': [], 'Electrocute_Damage': [], 'Energy_Leech_Chance': [], 'pets_Fire_Damage': [],
                   'Energy_Absorbed_From_Enemy_Spells': [], 'Physical_Resistance': [], 'Offensive_Ability': [],
                   'Total_Speed': [], 'Energy_Regenerated_per_Second': [], 'Chance_of_Impaired_Aim_to_Target': [],
                   'Health_Regenerated_Per_Second': [], 'Increases_Health_Regeneration': [],
                   'pet_Vitality_Resistance': [], 'Crit_Damage': [],  'pets_Elemental_Resistance': [],
                   'pets_Bleeding_Damage': [], 'pets_of_Attack_Damage_Converted_To_Health': [],
                   'of_Attack_Damage_Converted_To_Health': [],  'bleed_Seconds_Duration_reduction': []}


class Constellation:
    """
    This is a class that represents the in-game constellation.
    """

    def __init__(self, name, affinity_bonus, requirement, members, requirement_ready=False, missing_points=None,
                 unlocked=False, tier=1, requir_met=None, requir_met_two=None, updated_requirement=None,
                 requir_met_three=None):
        """
        :param name: Name of a constellation, e.g. Panther.
        :param affinity_bonus: The bonus to affinities that is added upon unlocking all stars of a constellation.
        :param requirement: The number of affinity points that has to be met to unlock the first star of a
        constellation.
        :param members: A list of stars objects which make up a constellation.
        :param requirement_ready: Defines if affinity requirement has been met.
        :param missing_points: Defines how many affinity points are still missing. Once method see_missing_points is
        called self.missing points is turned into a dictionary with affinity types as keys and missing points as values.
        :param unlocked: Defines if the first star of a constellation has been unlocked.
        :param tier: There are three tiers, the higher the tier the more affinity points is required to unlock a
        constellation
        :param requir_met: Defines if the first affinity requirement is met. This affinity is equal to whatever affinity
        is specified as first in self.requirement.
        :param requir_met_two: Defines if the second affinity requirement is met.
        :param updated_requirement: The dictionary with updated requirement values.
        :param requir_met_three: Defines if the second affinity requirement is met.
        """
        self.name = name
        self.members = members
        self.affinity_bonus = affinity_bonus
        self.requirement = requirement
        self.requirement_ready = requirement_ready
        self.missing_points = missing_points
        self.unlocked = unlocked
        self.tier = tier
        self.requir_met = requir_met
        self.requir_met_two = requir_met_two
        self.requir_met_three = requir_met_three
        self.updated_requirement = updated_requirement

    def __repr__(self):
        return '{}'.format(self.name)

    def see_missing_points(self,  requir=None):
        """
        Check how many affinity points has to be gained in order to meet the star(self) requirement.
        :param requir: The one speific affinity to check.
        :return: The dictionary with affinities as keys and missing points as values.
        """

        if self.requirement[requir] - eval(requir).points > 0:
            return {requir: self.requirement[requir] - eval(requir).points}
        else:
            return {requir: 'no missing affinity points'}

    def update_status(self):
        """
        Check if the affinity requirements are met so that unlocking of all stars in a constellation can be done.
        :return: True if the affinity requirements are met.
        """

        bool_list = []

        for i in self.requirement:
            # Append True or False to bool_list depending on a requirement being met or not.
            if type(self.requirement[i]) != list:
                bool_list.append(eval(i).points >= self.requirement[i])
            else:
                bool_list.append(eval(i).points >= self.requirement[i][0])
        # fast_mode and standard_mode can be executed multiple times. If so affinities pools must be different
        # than zero, consequently the real affinity requirement for a star is equal to the value stored in
        # self.requirement minus the current affinity pool. The below blocks of code evaluate which affinity
        # requirement have already been met, which will be used later on to create the updated self.requirement
        # dictionary(update_requirement method).
        if type(self.requirement[list(self.requirement.keys())[0]]) == list:
            req = self.requirement[list(self.requirement.keys())[0]][0]
            if req <= eval(list(self.requirement.keys())[0]).points:
                self.requir_met = req
        else:
            if self.requirement[list(self.requirement.keys())[0]] <= eval(list(self.requirement.keys())[0]).points:
                self.requir_met = list(self.requirement.keys())[0]
        if len(self.requirement) > 1:
            if type(self.requirement[list(self.requirement.keys())[1]]) == list:
                req_two = self.requirement[list(self.requirement.keys())[1]][0]
                if req_two <= eval(list(self.requirement.keys())[1]).points:
                    self.requir_met_two = req_two
            else:
                if self.requirement[list(self.requirement.keys())[1]] <= eval(list(self.requirement.keys())[1]).points:
                    self.requir_met_two = list(self.requirement.keys())[1]
        if len(self.requirement) > 2:
            if type(self.requirement[list(self.requirement.keys())[2]]) == list:
                req_three = self.requirement[list(self.requirement.keys())[2]][0]
                if req_three <= eval(list(self.requirement.keys())[2]).points:
                    self.requir_met_three = req_three
            else:
                if self.requirement[list(self.requirement.keys())[2]] <= eval(list(self.requirement.keys())[2]).points:
                    self.requir_met_three = list(self.requirement.keys())[2]
        if False in bool_list:
            self.requirement_ready = False
        else:
            self.requirement_ready = True
        return self.requirement_ready

    def update_requirement(self):
        """
        In case of one or two affinities of a constellation requirement being unlocked, the method creates a new
        dictionary with an updated set of required affinities.
        :return: updated constellation requirement
        """
        self.updated_requirement = {}
        list_of_keys = list(self.requirement.keys())

        if self.requir_met:
            for i in list(self.requirement.keys()):
                if i == self.requir_met:
                    list_of_keys.remove(i)
        if self.requir_met_two:
            for i in list(self.requirement.keys()):
                if i == self.requir_met_two:
                    list_of_keys.remove(i)
        if self.requir_met_three:
            for i in list(self.requirement.keys()):
                if i == self.requir_met_three:
                    list_of_keys.remove(i)
        for i in list_of_keys:
            self.updated_requirement[i] = self.requirement[i]
        if self.requir_met is None and self.requir_met_two is None and self.requir_met_three is None:
            return self.requirement
        return self.updated_requirement

    def requirs_reset(self):
        """
        Reset all dynamic requirements values to None. One of the functions enabling a user to start from the beginning
        without having to refresh the page.
        :return: Confirmation of successful execution.
        """
        self.requir_met = None
        self.requir_met_two = None
        self.requir_met_three = None
        return True

    def unlock_fast(self):
        """
        Unlock all stars in a constellation.
        :return: The list of unlocked stars.
        """

        # First confirm that all requirements ave been met.
        self.update_status()
        if self.requirement_ready and self.unlocked is False:
            list(map(lambda a: a.unlock(), self.members))
            list(map(lambda a: a.add_bonus(), self.members))
            self.add_affinity_bonus()
            self.unlocked = True
            # Set minimum value of a particular affinity type points below which the program cannot go so that all stars
            # remain in unlocked state.
            for affinity in affinities:
                if affinity.name in self.requirement:
                    affinity.set_minimum(self.requirement[affinity.name])
        return unlocked_stars

    def reset_unlock_status(self):
        """
        Sets unlock status back to false so that a star can be unlocked again.
        :return: self.unlocked = false(information that a star can be unlocked)
        """
        self.unlocked = False
        return self.unlocked

    def check_full(self):
        """
        The method checks if all stars of a constellation are unlocked.
        :return: True if all stars of a constellation are unlocked.
        """
        counter = 0
        for i in self.members:
            if i in unlocked_stars:
                counter += 1
        if counter == len(self.members):
            return True
        else:
            return False

    def add_affinity_bonus(self):
        """
        Add affinity bonus of a constellation to affinity points pool.
        :return: Confirmation of execution(True).
        """
        if self.check_full():
            for i in self.affinity_bonus:
                if self.affinity_bonus:
                    eval(i).add_points(self.affinity_bonus[i])
        return True

    def unlock_till_star(self, st):
        """
        Iterates over stars of a constellation and unlocks only those which are necessary to reach one particular star,
        then unlocks the star(parameter) and stops the process.
        :param st: The star to unlock.
        :return: True if the star has been unlocked.
        """

        counter = 0
        for member in self.members:
            if member.line == st.line or member.line is None and member.rank <= st.rank:
                member.unlock()
                member.add_bonus()
                counter += 1
                # Set minimum value of a particular affinity type points below which the program cannot go so that all
                # stars remain in unlocked state.
                if st in unlocked_stars:
                    for aff in self.requirement:
                        eval(aff).set_minimum(self.requirement[aff])
                    break
        # Add affinity bonus only if all stars of a constellation have been unlocked.
        if counter == len(self.members):
            self.add_affinity_bonus()
        return st in unlocked_stars

    def update_unlock_status(self):
        """
        Checks if all stars of a constellation have been unlocked.
        :return: True or False.
        """
        for i in self.members:
            if i in unlocked_stars:
                self.unlocked = True
            else:
                self.unlocked = False
        return self.unlocked


class Possibility:
    """
    There are many ways to unlock a constellation of a user's choice. This object helps to determine how to reach the
    constellation using the least in-game devotion points as possible.
    """
    def __init__(self, name, number_repr, affinity, options=None, selected=None, variety=1, var_one=None, var_two=None,
                 var_three=None, var_four=None, vars_to_asses=None, secondary=None,
                 tertiary=None):
        """
        :param name: a string made of a dictionary containing affinity name as key and possible points variations.
        :param number_repr: a dictionary containing affinity name as key and possible points variations.
        For example, if a constellation requires 10 points of primordial affinity, the possible variation are 5,5 or
        4, 6. number_repr stores only one variation.
        :param affinity: The affinity to which a variation relates.
        :param options: constellations which grant affinity bonus equal to or higher than the number specified in
        number_repr.
        :param selected: constellations which have enough affinity bonus and the lowest requirement possible.
        :param variety: variety tells how many unique numbers there are in number_repr.
        :param var_one: The first unique item.
        :param var_two: The second unique item.
        :param var_three: The third unique item.
        :param var_four: The fourth unique item.
        :param vars_to_asses:
        :param secondary: The second affinity required to unlock a star.
        :param tertiary: The third affinity required to unlock a star.
        """
        self.name = name
        self.number_repr = number_repr
        self.affinity = affinity
        self.options = options
        self.selected = selected
        self.variety = variety
        self.var_one = var_one
        self.var_two = var_two
        self.var_three = var_three
        self.var_four = var_four
        self.vars_to_asses = vars_to_asses
        self.secondary = secondary
        self.tertiary = tertiary

    def __repr__(self):
        return self.name

    def update_options(self, const_list, affinity, second, third, two_requirements=False):
        """
        Pick constellations which grant affinity bonus equal or higher than the numbers in number_repr.
        :param const_list: The list of constellations.
        :param affinity: The first affinity needed to unlock the constellation.
        :param two_requirements: Determines if a constellation has at least two affinity requirements.
        :param second: Second affinity.
        :param third: Third affinity.
        :return: Constellations which affinity bonus is equal or higher than the numbers in number_repr.
        """
        self.options = []
        # Limit the constellations list to those constellations which grant the best affinity bonus relatively to the
        # number of their devotion points requirement.
        const_list = [x for x in const_list if x.tier == 1]
        if two_requirements:
            for i in self.number_repr:
                for lst in i.values():
                    for num in lst:
                        for item in const_list:
                            if affinity in item.affinity_bonus and item.affinity_bonus[affinity] >= num:
                                self.options.append(item)
                            elif second in item.affinity_bonus and \
                                    item.affinity_bonus[second] >= num:
                                self.options.append(item)
                            elif third in item.affinity_bonus and \
                                    item.affinity_bonus[third] >= num:
                                self.options.append(item)
        else:
            for item in const_list:
                if affinity in item.affinity_bonus:
                    for num in self.number_repr[affinity]:
                        if item.affinity_bonus[affinity] >= num:
                            self.options.append(item)
        self.options = list(set(self.options))
        return self.options

    def pick_matching_options(self, var, aff):
        """
        The program goes through a list of potential constellations in order to find the ones which grant affinity bonus
        equal or higher than the first item of var list.
        :param var: this is self.var - self.var_six depending on the star affinity requirement and the current
        possibility.
        :param aff: The affinity that the program is currently working on.
        :return: Temp list with constellations which affinity bonus is equal or higher than the searched ones specified
        in self.number_repr.
        """
        temp = []

        for i in self.options:
            if i.affinity_bonus[aff] >= var[0]:
                temp.append(i)
        temp = list(set(temp))
        if self.selected:
            for i in temp:
                if i in self.selected:
                    temp.remove(i)
        # The number of collected constellations cannot be lower than the minimum required specified in var[1].
        if len(temp) < var[1]:
            return None
        else:
            return temp

    def update_selected(self, aff):
        """
        Select the best constellation(the least devotion points required with minimum x affinity bonus) for all values
        specified in self.number_repr(self_var_one-var_six).
        :param aff: All the numbers relate to one specific affinity.
        :return: A list with the best constellations to unlock.
        """
        self.update_vars(self.vars_to_asses)
        if self.variety == 1:
            self.pick_best_constellations(self.options, aff, self.number_repr[aff][0], var=len(self.number_repr[aff]))
        # In case of diversity in affinity bonuses of available options the program needs to identify the differences
        # first.
        elif self.variety == 2:
            best_one = self.pick_matching_options(self.var_one, aff)
            best_two = self.pick_matching_options(self.var_two, aff)
            if self.var_one[1] > 1:
                if best_one:
                    self.pick_best_constellations(best_one, aff, self.var_one[0], var=self.var_one[1])
                else:
                    return None
            if self.var_one[1] == 1:
                if best_one:
                    self.pick_best_constellations(best_one, aff, self.var_one[0], var=self.var_one[1])
                else:
                    return None
            if self.var_two[1] > 1:
                if best_two:
                    self.pick_best_constellations(best_two, aff, self.var_two[0], var=self.var_two[1])
                else:
                    return None
            if self.var_two[1] == 1:
                if best_two:
                    self.pick_best_constellations(best_two, aff, self.var_two[0], var=self.var_two[1])
                else:
                    return None

        elif self.variety == 3:
            best_one = self.pick_matching_options(self.var_one, aff)
            best_two = self.pick_matching_options(self.var_two, aff)
            best_three = self.pick_matching_options(self.var_three, aff)
            # Check if the first needed affinity is present in the affinity value dict, then check how many
            # constellations with the given affinity_bonus need to be unlocked.
            if self.var_one[1] > 1:
                if best_one:
                    self.pick_best_constellations(best_one, aff, self.var_one[0], var=self.var_one[1])
                else:
                    return None
            if self.var_one[1] == 1:
                if best_one:
                    self.pick_best_constellations(best_one, aff, self.var_one[0], var=self.var_one[1])
                else:
                    return None
            if self.var_two[1] > 1:
                if best_two:
                    self.pick_best_constellations(best_two, aff, self.var_two[0], var=self.var_two[1])
                else:
                    return None
            if self.var_two[1] == 1:
                if best_two:
                    self.pick_best_constellations(best_two, aff, self.var_two[0], var=self.var_two[1])
                else:
                    return None
            if self.var_three[1] > 1:
                if best_three:
                    self.pick_best_constellations(best_three, aff, self.var_three[0], var=self.var_three[1])
                else:
                    return None
            if self.var_three[1] == 1:
                if best_three:
                    self.pick_best_constellations(best_three, aff, self.var_three[0], var=self.var_three[1])
                else:
                    return None

        elif self.variety == 4:
            best_one = self.pick_matching_options(self.var_one, aff)
            best_two = self.pick_matching_options(self.var_two, aff)
            best_three = self.pick_matching_options(self.var_three, aff)
            best_four = self.pick_matching_options(self.var_four, aff)
            # Check if the first needed affinity is present in the affinity value dict, then check how many
            # constellations with the given affinity_bonus need to be unlocked.
            if self.var_one[1] > 1:
                if best_one:
                    self.pick_best_constellations(best_one, aff, self.var_one[0], var=self.var_one[1])
                else:
                    return None
            if self.var_one[1] == 1:
                if best_one:
                    self.pick_best_constellations(best_one, aff, self.var_one[0], var=self.var_one[1])
                else:
                    return None
            if self.var_two[1] > 1:
                if best_two:
                    self.pick_best_constellations(best_two, aff, self.var_two[0], var=self.var_two[1])
                else:
                    return None
            if self.var_two[1] == 1:
                if best_two:
                    self.pick_best_constellations(best_two, aff, self.var_two[0], var=self.var_two[1])
                else:
                    return None
            if self.var_three[1] > 1:
                if best_three:
                    self.pick_best_constellations(best_three, aff, self.var_three[0], var=self.var_three[1])
                else:
                    return None
            if self.var_three[1] == 1:
                if best_three:
                    self.pick_best_constellations(best_three, aff, self.var_three[0], var=self.var_three[1])
                else:
                    return None
            if self.var_four[1] > 1:
                if best_four:
                    self.pick_best_constellations(best_four, aff, self.var_four[0], var=self.var_four[1])
                else:
                    return None
            if self.var_four[1] == 1:
                if best_four:
                    self.pick_best_constellations(best_four, aff, self.var_four[0], var=self.var_four[1])
                else:
                    return None
        return self.selected

    def update_vars(self, vars_to_asses):
        """
        The method determines how many different numbers(affinity bonus values) there are in self.number_repr as well as
        number of occurrences of a particular affinity bonus value. This way the program knows how many constellations
        needs to be unlocked. For example, if there is two 'fives' in self.number_repr, the program will eventually
        unlock two constellations both with affinity bonus equal to five.
        :return: a tuple with lists as elements. Lists contain particular affinity bonus value at index 0 and number of
        its occurrences in self.number_repr.
        """
        unique = list(set(vars_to_asses))
        unique.sort(reverse=True)
        self.vars_to_asses = vars_to_asses
        if self.variety == 1:
            self.var_one = [unique[0], vars_to_asses.count(unique[0])]
            return self.var_one
        elif self.variety == 2:
            self.var_one = [unique[0], vars_to_asses.count(unique[0])]
            self.var_two = [unique[1], vars_to_asses.count(unique[1])]
            return self.var_one, self.var_two
        elif self.variety == 3:
            self.var_one = [unique[0], vars_to_asses.count(unique[0])]
            self.var_two = [unique[1], vars_to_asses.count(unique[1])]
            self.var_three = [unique[2], vars_to_asses.count(unique[2])]
            return self.var_one, self.var_two, self.var_three
        elif self.variety == 4:
            self.var_one = [unique[0], vars_to_asses.count(unique[0])]
            self.var_two = [unique[1], vars_to_asses.count(unique[1])]
            self.var_three = [unique[2], vars_to_asses.count(unique[2])]
            self.var_four = [unique[3], vars_to_asses.count(unique[3])]
            return self.var_one, self.var_two, self.var_three, self.var_four

    def pick_best_constellations(self, temp_list, affinity_type, minimum_affinity, var=None):
        """
        The method uses series of filters in order to find the best constellations to unlock.
        :param temp_list: A list of constellations ready for the final selection.
        :param affinity_type: The affinity type, e.g. primordial.
        :param minimum_affinity: If the minimum affinity bonus is equal 5, the program cannot pick anything under this
        value.
        :param var: Number of constellations to pick in order to meet a star's affinity requirement.
        :return: An updated temp_list.
        """
        counter = 0
        if self.selected is None:
            self.selected = []
        temp_list = [x for x in temp_list if x not in self.selected]
        temp_list = list(set(temp_list))
        # Number of members of a constellation define how many devotion points is needed to unlock the constellation.
        temp_list.sort(key=lambda a: len(a.members))
        stars_const = None
        if type(star) == Star:
            stars_const = star.find_constellation()
        else:
            stars_const = star

        # Determine the best constellation to unlock.
        best_option = temp_list[0]
        if best_option in self.selected and len(self.selected) > 1:
            best_option = temp_list[1]
        else:
            best_option = temp_list[0]
        for option in temp_list:
            if option in self.selected:
                continue
            # In case there are more items in temp_list with the same devotion points requirement, pick the one with
            # higher affinity bonus.
            if len(option.members) == len(best_option.members) and option.affinity_bonus[affinity_type] > \
                    minimum_affinity and option not in self.selected:
                best_option = option
            if option not in self.selected and best_option not in self.selected:
                self.selected.append(best_option)
        temp_list.remove(best_option)
        counter += 1
        # When counter reaches the value of var it means that all needed constellations have been selected.
        while counter < var:
            for option in temp_list:
                if counter == var or len(temp_list) + 1 < var:
                    break
                if len(best_option.members) == 1 and option not in self.selected:
                    self.selected.append(min(temp_list, key=lambda a: len(a.members)))
                    counter += 1
                if len(option.members) == len(best_option.members) and option.affinity_bonus[affinity_type] >= \
                        minimum_affinity and option not in self.selected:
                    counter += 1
                    self.selected.append(option)
                elif len(option.members) - 1 == len(best_option.members) and option.affinity_bonus[affinity_type] >= \
                        minimum_affinity and option not in self.selected:

                    counter += 1
                    self.selected.append(option)
                elif len(option.members) - 2 == len(best_option.members) and option.affinity_bonus[affinity_type] >= \
                        minimum_affinity and option not in self.selected:
                    counter += 1
                    self.selected.append(option)
        return self.selected

    def define_variety(self):
        """
        Series of operations with the aim of defining self.variety, that is the number of unique affinity values needed
        to unlock the clicked star.
        :return: the number of unique affinity values needed to unlock the clicked star.
        """
        to_define = []
        to_define.extend(list(self.number_repr.values()))
        to_define = [j for i in to_define for j in i]
        self.vars_to_asses = to_define
        to_define = list(set(to_define))
        self.variety = len(to_define)
        return self.variety


class FastMode:
    """
    FastMode takes possibilities created and preselected by Possibility object. It evaluates how many devotion points is
    needed to follow the path of a specific possibility than the program compares the result against other FastMode
    objects to find the one that requires the least devotion points.
    """
    def __init__(self, name, poss_one, primary, poss_two=None, poss_three=None, merged=None, secondary=None,
                 secondary_points=None, tertiary=None, tertiary_points=None):
        """
        :param name: It is always the name of the star to unlock.
        :param poss_one: The proposed method to unlock the star. It might rare, standard or mixed method.
        Rare looks for constellations with affinity bonuses to two types of affinity requirement.
        Standard looks for constellations with one affinity bonus.
        Mixed uses standard and rare method.
        :param primary: The first affinity type of the constellation's requirement.
        :param poss_two: The proposed method to gain enough affinity points of the second type.
        :param poss_three: The proposed method to gain enough affinity points of the third type.
        :param merged: A list with all given methods(poss_one, two, three).
        :param secondary: The second affinity type of the constellation's requirement.
        :param secondary_points:
        :param tertiary: The third affinity type of the constellation's requirement.
        :param tertiary_points:
        """
        self.name = name
        self.poss_one = poss_one
        self.poss_two = poss_two
        self.poss_three = poss_three
        self.merged = merged
        self.primary = primary
        self.secondary = secondary
        self.secondary_points = secondary_points
        self.tertiary = tertiary
        self.tertiary_points = tertiary_points

    def __repr__(self):
        return self.name

    def evaluate_secondary_points(self, points, possibility):
        """
        The program goes through a list of constellations to unlock(possibility) in order to determine if any of them
        grants a bonus to the second affinity(points parameter). If so, the constellation's missing_points attribute is
        updated.
        :param points: Affinity type.
        :param possibility: The chosen way to meet the affinity requirement.
        :return: Number of affinity points.
        """
        result = []
        counter = 0
        if type(star) == Star:
            star_const = star.find_constellation()
        else:
            star_const = star
        for i in possibility:
            if type(i) != int and points and points in i.affinity_bonus:
                result.append(i)
        for i in result:
            counter += i.affinity_bonus[points]
        if type(star_const.see_missing_points(requir=points)[points]) != str:
            points = star_const.see_missing_points(requir=points)[points] - counter
        return points

    def update_poss(self, poss_two):
        """
        Updates the object with the possibility that consumes the least devotion points.
        :param poss_two: one of the possible ways to unlock the clicked star.
        :return: Updated possibility.
        """

        self.poss_two = poss_two
        return self.poss_two

    def merge_possibilities(self):
        """
        Create a list made of all constellations to unlock based on the object possibilities.
        :return: The list of all constellations needed to unlock a star.
        """
        if type(star) == Star:
            star_const = star.find_constellation()
        else:
            star_const = star
        self.merged = []
        self.poss_one = [x for x in self.poss_one if type(x) == Constellation]
        if len(star_const.updated_requirement) > 1:
            self.poss_two = [x for x in self.poss_two if type(x) == Constellation]
            self.merged.extend(self.poss_one)
            self.merged.extend(self.poss_two)
        if len(star_const.updated_requirement) > 2:
            self.poss_two = [x for x in self.poss_two if type(x) == Constellation]
            self.poss_three = [x for x in self.poss_three if type(x) == Constellation]
            self.merged.extend(self.poss_one)
            self.merged.extend(self.poss_two)
            self.merged.extend(self.poss_three)
        if self.merged is False:
            self.merged.extend(self.poss_one)
        return self.merged

    def calculate_devpoints(self, joiners):
        """
        The method calculates the number of devotion points needed to unlock merged possibilities, that is all
        constellations which altogether give enough affinity bonus to unlock the clicked star.
        :return:
        """
        devpoints_needed = 0
        crossroads_points = 0
        if self.merged:
            for constellation in self.merged:
                devpoints_needed += len(constellation.members)
                if 'Crossroads' in constellation.name:
                    crossroads_points += 1
            devpoints_needed = devpoints_needed - (joiners - crossroads_points)
        else:
            return devpoints_needed + 100
        return devpoints_needed


# THIS SECTION IS DEDICATED TO CREATING INSTANCES OF STARS AND CONSTELLATIONS OBJECTS. There are 96 constellations.
# One constellation has at least 3 stars and can have as many as 8 stars.
# NAMING PATTERN FOR CROSSROADS: first two letters 'cs' mean crossroads, the rest of the name refers to affinity.

cschaos = Star('Crossroads_of_Chaos', 'Crossroads Of Chaos', [0], [Points_of_Chaos], [1], 0, rank=0, Health=5/100,
               affinity=True)
crossroads_of_chaos = Constellation('Crossroads_of_Chaos', {Points_of_Chaos.name: 1}, {Points_of_Chaos.name: 0},
                                    [cschaos])
csasc = Star('Crossroads_of_Ascendant', 'Crossroads Of Ascendant', [0], [Points_of_Ascendant], [1], 0, rank=0,
             Offensive_Ability=18, affinity=True)
crossroads_of_ascendant = Constellation('Crossroads_of_Ascendant', {Points_of_Ascendant.name: 1},
                                        {Points_of_Ascendant.name: 0}, [csasc])
csord = Star('Crossroads_of_Order', 'Crossroads Of Order', [0], [Points_of_Order], [1], 0, rank=0, Health=5/100,
             affinity=True)
crossroads_of_order = Constellation('Crossroads_of_Order', {Points_of_Order.name: 1}, {Points_of_Order.name: 0},
                                    [csord])
csprim = Star('Crossroads_of_Primordial', 'Crossroads Of Primordial', [0], [Points_of_Primordial], [1], 0, rank=0,
              Defensive_Ability=18, affinity=True)
crossroads_of_primordial = Constellation('Crossroads_of_Primordial', {Points_of_Primordial.name: 1},
                                         {Points_of_Primordial.name: 0}, [csprim])
cseld = Star('Crossroads_of_Eldritch', 'Crossroads Of Eldritch', [0], [Points_of_Eldritch], [1], 0, rank=0,
             Offensive_Ability=18, affinity=True)
crossroads_of_eldritch = Constellation('Crossroads_of_Eldritch', {Points_of_Eldritch.name: 1},
                                       {Points_of_Eldritch.name: 0}, [cseld])

# NAMING PATTERN FOR ALL OTHER STARS: The first few letters refer to constellations' names, the last one/two letters
# refer to the place that a star has in the structure of a constellations. Letter 'f' in the end mean 'first', 's' -
# 'second', 't' - third, and so on. Stars which grant skills are named similarly to their in-game names.

tortof = Star('Tortoise', 'First Tortoise Star', [1], [Points_of_Primordial, Points_of_Order], [3, 2],
              [Points_of_Order], rank=0, Health=25, Defensive_Ability=12)
tortos = Star('Tortoise', ' Second Tortoise Star ', Defensive_Ability=15, rank=1,
              Physique_Requirement_For_Shields=10/100)
tortot = Star('Tortoise', ' Third Tortoise Star ', rank=2, Health=100, Defensive_Ability=15)
tortoft = Star('Tortoise', ' Fourth Tortoise Star ', line=1, rank=3, Health=4/100, Defensive_Ability=10, Armor=4/100)
turtle_shell = Star('Tortoise', 'Turtle Shell', line=3, rank=3, Seconds_Skill_Recharge=12, Damage_Absorption=5150)
tortoise = Constellation(tortof.source, {Points_of_Primordial.name: tortof.bonus_value[0],
                                         Points_of_Order.name: tortof.bonus_value[1]},
                         {Points_of_Order.name: tortof.unlockr[0]},
                         [tortof, tortos, tortot, tortoft, turtle_shell])

sailof = Star('Sailor_Guide', 'First Sailors Guide Star', [1], [Points_of_Primordial], [5], [Points_of_Primordial],
              rank=0, Physique=15, Defensive_Ability=8)
sailos = Star('Sailor_Guide', ' Second Sailors Guide Star ', rank=1, Reduced_Freeze_Duration=18/100,
              Slow_Resistance=18/100)
sailot = Star('Sailor_Guide', ' Third Sailors Guide Star ', line=1, rank=2, Physical_Resistance=3/100,
              Cold_Resistance=15/100, Lightining_Resistance=15/100)
sailoft = Star('Sailor_Guide', ' Fourth Sailors Guide Star ', line=2, rank=2, Physique=15, Movement_Speed=8/100)
sailor_guide = Constellation(sailof.source, {Points_of_Primordial.name: sailof.bonus_value[0]},
                             {str(Points_of_Primordial.name): sailof.unlockr[0]}, [sailof, sailos, sailot, sailoft])

tsunaf = Star('Tsunami', 'First Tsunami Star', [1], [Points_of_Primordial], [5], [Points_of_Primordial], rank=0,
              Cold_Damage=15/100, Lightining_Damage=15/100)
tsunas = Star('Tsunami', ' Second Tsunami Star ', rank=1, Spirit=15, Defensive_Ability=10)
tsunat = Star('Tsunami', ' Third Tsunami Star ', rank=2, Frostburn_Damage=40/100, Electrocute_Damage=40/100,
              Physique=15)
tsunaft = Star('Tsunami', ' Fourth Tsunami Star ', rank=3, Cold_Damage=24/100, Lightining_Damage=24/200)
tsunami_skill = Star('Tsunami', 'Tsunami skill', rank=4, Seconds_Skill_Recharge=1, Meter_Range=12, Weapon_Damage=34/100,
                     Cold_Damage=range(180, 215), Lightining_Damage=range(82, 130), Frostburn_Damage=282,
                     Chance_for_Target_to_Fumble_Attacks=14/100, Chance_of_Impaired_Aim_to_Target=14/100)
tsunami = Constellation('Tsunami', {Points_of_Primordial.name: sailof.bonus_value[0]},
                        {str(Points_of_Primordial.name): sailof.unlockr[0]},
                        [tsunaf, tsunas, tsunat, tsunaft, tsunami_skill])

impf = Star('Imp', 'First Imp Star', [1], [Points_of_Primordial, Points_of_Eldritch], [3, 3], [Points_of_Primordial],
            rank=0, Fire_Damage=15/100, Aether_Damage=15/100)
imps = Star('Imp', ' Second Imp Star ', rank=1, Spirit=15, Defensive_Ability=10)
impt = Star('Imp', ' Third Imp Star ', rank=2, Aether_Resistance=8/100, Physique=15)
impft = Star('Imp', ' Fourth Imp Star ', rank=3, Fire_Damage=24/100, Aether_Damage=24/100)
aetherfire = Star('Imp', ' Aetherfire ', rank=4, Second_Duration=3, Meter_Radius=2.5, Fire_Damage=140,
                  Aether_Damage=165, Chance_to_Confuse=[33/100, 2])
imp = Constellation('Imp', {Points_of_Primordial.name: impf.bonus_value[0],
                    Points_of_Eldritch.name: impf.bonus_value[1]}, {Points_of_Primordial.name: impf.unlockr[0]},
                    [impf, imps, impt, impft, aetherfire])

falcof = Star('Falcon', 'First Falcon Star', [1], [Points_of_Ascendant, Points_of_Eldritch], [3, 3],
              [Points_of_Ascendant], rank=0, Physical_Damage=15/100, Bleeding_Damage=15/100)
falcos = Star('Falcon', 'Second Falcon Star', rank=1, Health=60, Offensive_Ability=15)
falcot = Star('Falcon', 'Third Falcon Star', rank=2, Cunning=20)
falcoft = Star('Falcon', ' Fourth Falcon Star ', rank=3, Physical_Damage=24/100, Bleeding_Damage=24/100)
falcon_swoop = Star('Falcon', 'Falcon Swoop', rank=4, Meter_Radius=0.1, Seconds_Skill_Recharge=2, Projectiles=6,
                    Weapon_Damage=24/100, Physical_Damage=116, Bleeding_Damage=525,
                    Chance_to_pass_through_Enemies=100/100)
falcon = Constellation('Falcon', {Points_of_Ascendant.name: falcof.bonus_value[0],
                       Points_of_Eldritch.name: falcof.bonus_value[1]}, {Points_of_Ascendant.name: falcof.unlockr[0]},
                       [falcof, falcos, falcot, falcoft, falcon_swoop])

ratf = Star('Rat', 'First Rat Star', [1], [Points_of_Eldritch, Points_of_Chaos], [3, 2], [Points_of_Chaos], rank=0,
            Cunning=15, Spirit=15)
rats = Star('Rat', ' Second Rat Star ', rank=1, Poison_Damage=[40, 24/100], Acid_Retaliation=20)
ratt = Star('Rat', ' Third Rat Star ', rank=2, Cunning=20, Spirit=20, Acid_Retaliation=30,
            Poison_and_Acid_Resistance=10/100)
ratft = Star('Rat', ' Fourth Rat Star ', rank=3, Poison_Damage=[60, 50/100], to_All_Retaliation_Damage=25/100)
rat = Constellation('Rat', {Points_of_Eldritch.name: ratf.bonus_value[0], Points_of_Chaos.name: ratf.bonus_value[1]},
                    {str(Points_of_Chaos.name): ratf.unlockr[0]}, [ratf, rats, ratt, ratft])

cranef = Star('Crane', 'First Crane Star', [1], [Points_of_Order], [5], [Points_of_Order], rank=0, Physique=15,
              Spirit=15)
cranes = Star('Crane', ' Second Crane Star ', rank=1, Poison_and_Acid_Resistance=12/100,
              pets_Poison_and_Acid_Resistance=12)
cranet = Star('Crane', ' Third Crane Star ', rank=2, to_All_Damage=15/100, Spirit_req_weapons=10/100)
craneft = Star('Crane', ' Fourth Crane Star ', rank=3, Vitality_Resistance=12/100, pets_Vitality_Resistance=12/100)
craneff = Star('Crane', ' Fifth Crane Star ', rank=4, Elemental_Resistance=16/100, Bleeding_Resistance=16/100,
               Reflected_Damage_Reduction=22/100)
crane = Constellation('Crane', {Points_of_Order.name: cranef.bonus_value[0]},
                      {Points_of_Order.name: cranef.unlockr[0]}, [cranef, cranes, cranet, craneft, craneff])

liof = Star('Lion', 'First Lion Star', [1], [Points_of_Order], [3], [Points_of_Order], rank=0, Health=4/100,
            pets_Health=3/100, Defensive_Ability=8)
lios = Star('Lion', ' Second Lion Star ', rank=1, Spirit=15, Movement_Speed=3/100, Health=100)
liot = Star('Lion', ' Third Lion Star ', rank=2, to_All_Damage=15/100, Physical_Resistance=2/100,
            pets_to_All_Damage=12/100)
lion = Constellation('Lion', {Points_of_Order.name: liof.bonus_value[0]}, {Points_of_Order.name: liof.unlockr[0]},
                     [liof, lios, liot])

bullf = Star('Bull', 'First Bull Star', [1], [Points_of_Primordial, Points_of_Order], [3, 2],
             [Points_of_Primordial], rank=0, Physique=15)
bulls = Star('Bull', ' Second Bull Star ', rank=1, Internal_Trauma_Damage=24/100, Movement_Speed=3/100)
bullt = Star('Bull', ' Third Bull Star ', rank=2, Physique=15,  Armor=30)
bullft = Star('Bull', ' Fourth Bull Star ', line=1, rank=3, Internal_Trauma_Damage=[60, 30/100],
              Physique_Requirement_for_Armor=-10/100)
bull_rush = Star('Bull', 'Bull Rush', line=2, rank=3, Seconds_Skill_Recharge=0.4, Meter_Target_Area=3.5,
                 Weapon_Damage=32/100, Physical_Damage=range(115, 230), Internal_Trauma_Damage=350)
bull = Constellation('Bull', {Points_of_Primordial.name: 3, Points_of_Order.name: 2}, {Points_of_Primordial.name: 1},
                     [bullf, bulls, bullt, bullft, bull_rush])

hounf = Star('Hound', 'First Hound Star', [1], [Points_of_Primordial], [4], [Points_of_Primordial], rank=0, Physique=15,
             pets_Health=4/100)
houns = Star('Hound', ' Second Hound Star ', rank=1, Armor=2/100, to_All_Retaliation_Damage=30/100)
hount = Star('Hound', ' Third Hound Star ', rank=2, Physique=20, Armor=5/100, to_All_Retaliation_Damage=40/100,
             pets_Health=8/100)
hound = Constellation('Hound', {Points_of_Primordial.name: 4}, {Points_of_Primordial.name: 1}, [hounf, houns, hount])

scaraf = Star('Scarab', 'First Scarab Star', [1], [Points_of_Primordial, Points_of_Order], [3, 2],
              [Points_of_Primordial], rank=0, Physique=15, Armor=20)
scaras = Star('Scarab', ' Second Scarab Star ', rank=1, Shield_Damage_Blocked=8/100)
scarat = Star('Scarab', ' Third Scarab Star ', line=1, rank=2, Bleeding_Resistance=15/100, Armor=4/100)
scaraft = Star('Scarab', ' Fourth Scarab Star ', line=2, rank=2, Reduced_Stun_Duration=15/100,
               Shield_Damage_Blocked=12/100, Acid_Retaliation=40)
scarab = Constellation('Scarab', {Points_of_Primordial.name: 3, Points_of_Order.name: 2},
                       {Points_of_Primordial.name: 1}, [scaraf, scaras, scarat, scaraft])

gallof = Star('Gallows', 'First Gallows Star', [1], [Points_of_Primordial], [5], [Points_of_Primordial], rank=0,
              Vitality_Damage=15/100, Chaos_Damage=15/100)
gallos = Star('Gallows', ' Second Gallows Star', rank=1, Health=3/100,  Bleeding_Resistance=10/100)
gallot = Star('Gallows', ' Third Gallows Star', rank=2, Health=80, Vitality_Resistance=10/100)
galloft = Star('Gallows', ' Fourth Gallows Star', rank=3, Vitality_Damage=[8, 24/100], Chaos_Damage=24/100,
               Damage_to_Humans=6/100)
gallows = Constellation('Gallows', {Points_of_Primordial.name: 5}, {Points_of_Primordial.name: 1},
                        [gallof, gallos, gallot, galloft])

lizaf = Star('Lizard', 'First Lizard Star', [1], [Points_of_Primordial], [4], [Points_of_Primordial], rank=0,
             Health_Regenerated_Per_Second=6, Constitution=15/100)
lizas = Star('Lizard', ' Second Lizard Star ', rank=1, Health_Regenerated_Per_Second=10, Health=50,
             Movement_Speed=3/100)
lizat = Star('Lizard', ' Third Lizard Star ', rank=2, Health=50, Healing_Effects_Increased=3/100,
             Increases_Health_Regeneration=25/100)
lizard = Constellation('Lizard', {Points_of_Primordial.name: lizaf.bonus_value[0]},
                       {Points_of_Primordial.name: lizaf.unlockr[0]}, [lizaf, lizas, lizat])

vipef = Star('Viper', 'First Viper Star', [1], [Points_of_Primordial, Points_of_Chaos], [3, 2], [Points_of_Chaos],
             rank=0, Cunning=15, Spirit=15)
vipes = Star('Viper', ' Second Viper Star ', rank=1, Energy_Leech_Chance=36, Energy_Absorbed_From_Enemy_Spells=10/100)
vipet = Star('Viper', ' Third Viper Star ', rank=2, Vitality_Resistance=10/100)
vipeft = Star('Viper', ' Fourth Viper Star ', rank=3, Reduced_target_Elemental_Resistances=20, Offensive_Ability=3/100)
viper = Constellation('Viper', {Points_of_Primordial.name: vipef.bonus_value[0],
                      Points_of_Chaos.name: vipef.bonus_value[1]},
                      {Points_of_Chaos.name: vipef.unlockr[0]}, [vipef, vipes, vipet, vipeft])


jackaf = Star('Jackal', 'First Jackal Star', [1], [Points_of_Chaos], [3], [Points_of_Chaos], rank=0, Energy=6/100,
              pets_Health=3/100)
jackas = Star('Jackal', ' Second Jackal Star ', rank=1, Offensive_Ability=12, Total_Speed=6/100)
jackat = Star('Jackal', ' Third Jackal Star ', rank=2, to_All_Damage=15/100, Physical_Resistance=2/100,
              pets_Attack_Speed=5/100)
jackal = Constellation('Jackal', {Points_of_Chaos.name: jackaf.bonus_value[0]}, {str(Points_of_Chaos.name):
                       jackaf.unlockr[0]}, [jackaf, jackas, jackat])

wref = Star('Wretch', 'First Wretch Star', [1], [Points_of_Primordial, Points_of_Chaos], [3, 2],
            [Points_of_Chaos], rank=0, Acid_Damage=15/100, Chaos_Damage=15/100)
wres = Star('Wretch', ' Second Wretch Star ', rank=1, Physique=15, Bleeding_Resistance=12/100)
wret = Star('Wretch', ' Third Wretch Star ', rank=2, Health=80, Defensive_Ability=15, Acid_Retaliation=30)
wreft = Star('Wretch', ' Fourth Wretch Star ', rank=3, Damage_to_Undead=6/100, Acid_Damage=24/100, Chaos_Damage=24/100)
wretch = Constellation('Wretch', {Points_of_Primordial.name: wref.bonus_value[0],
                       Points_of_Chaos.name: wref.bonus_value[1]}, {Points_of_Chaos.name: wref.unlockr[0]},
                       [wref, wres, wret, wreft])

batf = Star('Bat', 'First Bat Star', [1], [Points_of_Eldritch, Points_of_Chaos], [3, 2], [Points_of_Eldritch], rank=0,
            Vitality_Damage=15/100, Bleeding_Damage=15/100)
bats = Star('Bat', ' Second Bat Star ', rank=1, Vitality_Decay=30/100, Offensive_Ability=10)
batt = Star('Bat', ' Third Bat Star ', rank=2, Vitality_Damage=24/100, Bleeding_Damage=30/100)
batft = Star('Bat', ' Fourth Bat Star ', rank=3, Vitality_Damage=6, of_Attack_Damage_Converted_To_Health=3/100)
twin_fangs = Star('Bat', 'Twin Fangs', rank=4, Seconds_Skill_Recharge=0.6, Projectiles=2, Weapon_Damage=22/100,
                  Pierce_Damage=165, Vitality_Damage=range(128, 221), of_Attack_Damage_Converted_To_Health=40/100,
                  Chance_to_pass_through_Enemies=100/100)
bat = Constellation('Bat', {Points_of_Eldritch.name: batf.bonus_value[0], Points_of_Chaos.name: batf.bonus_value[1]},
                    {Points_of_Eldritch.name: batf.unlockr[0]}, [batf, bats, batt, batft, twin_fangs])

geyef = Star('Eye_Of_The_Guardian', 'First Eye Of The Guardian Star', [1], [Points_of_Ascendant, Points_of_Eldritch],
             [3, 3], [Points_of_Eldritch], rank=0, Acid_Damage=15/100, Poison_Damage=15/100)
geyes = Star('Eye_Of_The_Guardian', ' Second Eye Of The Guardian Star ', rank=1, Offensive_Ability=16,
             Defensive_Ability=16)
geyet = Star('Eye_Of_The_Guardian', ' Third Eye Of The Guardian Star ', rank=2, Chaos_Damage=20/100,
             Poison_Damage=15/100)
geyeft = Star('Eye_Of_The_Guardian', ' Fourth Eye Of The Guardian Star ', rank=3, Poison_Damage=30/100,
              Vitality_Resistance=8/100)
guardians_gaze = Star('Eye_Of_The_Guardian', "Guardian's Gaze", rank=4, Seconds_Skill_Recharge=0.5,
                      Chance_to_pass_through_Enemies=100/100, Meter_Radius=0.3, Weapon_Damage=15/100, Acid_Damage=83,
                      Chaos_Damage=193, of_Attack_Damage_Converted_To_Health=10/100, Poison_Damage=232)
eye_of_the_guardian = Constellation('Eye_Of_The_Guardian', {Points_of_Ascendant.name: geyef.bonus_value[0],
                                    Points_of_Eldritch.name: geyef.bonus_value[1]},
                                    {Points_of_Eldritch.name: geyef.unlockr[0]},
                                    [geyef, geyes, geyet, geyeft, guardians_gaze])

akerof = Star("Akerons_Scorpion", 'First Akerons Scorpion Star', [1], [Points_of_Eldritch], [5], [Points_of_Eldritch],
              rank=0, Offensive_Ability=12)
akeros = Star("Akerons_Scorpion", ' Second Akerons Scorpion Star ', rank=1, Physique=15, Poison_Damage=24/100,
              Acid_Damage=15/100)
akerot = Star("Akerons_Scorpion", ' Third Akerons Scorpion Star ', rank=2, Offensive_Ability=18)
akeroft = Star("Akerons_Scorpion", ' Fourth Akerons Scorpion Star ', line=1, rank=3, Acid_Damage=15/100,
               Poison_Damage=30/100)
scorpion_sting = Star("Akerons_Scorpion", 'Scorpion Sting', line=2, rank=3, Meter_Radius=0.1,
                      Seconds_Skill_Recharge=1.5, Projectiles=6, Weapon_Damage=40/100, Poison_Damage=725,
                      Reduced_target_Defensive_Ability=150, Chance_to_pass_through_Enemies=100/100)
akerons_scorpion = Constellation("Akerons_Scorpion", {Points_of_Eldritch.name: akerof.bonus_value[0]},
                                 {Points_of_Eldritch.name: akerof.unlockr[0]},
                                 [akerof, akeros, akerot, akeroft, scorpion_sting])

shepf = Star("Shepherds_Crook", 'First Shepherds Crook Star', [1], [Points_of_Ascendant], [5], [Points_of_Ascendant],
             rank=0, Health=40, pets_Health=8/100)
sheps = Star("Shepherds_Crook", ' Second Shepherds Crook Star ', rank=1, Cunning=15, Health=40)
shept = Star("Shepherds_Crook", ' Third Shepherds Crook Star ', rank=2, Elemental_Resistance=10/100,
             pets_Elemental_Resistance=15/100)
shepft = Star("Shepherds_Crook", ' Fourth Shepherds Crook Star ', rank=3, Health=3/100, pets_Health=5/100,
              pets_Defensive_Ability=5/100)
shepherd_call = Star("Shepherds_Crook", "Shepherds call", rank=4, Seconds_Skill_Recharge=6, Seconds_Duration=4,
                     Offensive_Ability=85, pets_to_All_Damage=250/100, pets_Crit_Damage=28/100,
                     pets_to_All_Retaliation_Damage=300/100)
shepherds_crook = Constellation("Shepherds_Crook", {Points_of_Ascendant.name: shepf.bonus_value[0]},
                                {Points_of_Ascendant.name: shepf.unlockr[0]},
                                [shepf, sheps, shept, shepft, shepherd_call])

talof = Star('Nightallon', 'First Nighttalon Star', [1], [Points_of_Ascendant, Points_of_Chaos], [3, 2],
             [Points_of_Ascendant], rank=0, Cunning=15, pets_to_All_Damage=15/100)
talos = Star('Nightallon', ' Second Nighttalon Star ', rank=1, Elemental_Resistance=10/100,
             pets_Elemental_Resistance=10/100)
talot = Star('Nightallon', ' Third Nighttalon Star ', line=1, rank=2, Bleeding_Damage=20/100,
             pets_Bleeding_Damage=12, pets_to_All_Damage=25/100)
taloft = Star('Nightallon', ' Fourth Nighttalon Star ', line=2, rank=2, Bleeding_Damage=50/100,
              pets_Bleeding_Damage=[24, 60/100], pets_Attack_Speed=5/100)
nightallon = Constellation("Nightallon", {Points_of_Ascendant.name: talof.bonus_value[0],
                                          Points_of_Chaos.name: talof.bonus_value[1]},
                           {Points_of_Ascendant.name: talof.unlockr[0]}, [talof, talos, talot, taloft])

anvif = Star('Anvil', 'First Anvil Star', [1], [Points_of_Ascendant], [5], [Points_of_Ascendant], rank=0,
             Defensive_Ability=15)
anvis = Star('Anvil', ' Second Anvil Star ', rank=1, Physique=20)
anvit = Star('Anvil', ' Third Anvil Star ', rank=2, Armor=30, Increases_Armor_Absorption=3/100)
anvift = Star('Anvil', ' Fourth Anvil Star ', rank=3, Internal_Trauma_Damage=40, Offensive_Ability=10,
              Defensive_Ability=15, Constitution=20/100)
targo_hammer = Star('Anvil', "Targos Hammer", rank=4, Seconds_Skill_Recharge=0.1,
                    Chance_to_pass_through_Enemies=100/100, Meter_Radius=0.3, Weapon_Damage=45/100,
                    of_Retaliation_Damage_added_to_Attack=16/100, Physical_Damage=203, Internal_Trauma_Damage=370/100,
                    Chance_to_Stun=[50/100, 1])
anvil = Constellation('Anvil', {Points_of_Ascendant.name: 5}, {Points_of_Ascendant.name: 1},
                      [anvif, anvis, anvit, anvift, targo_hammer])

hamef = Star('Hammer', 'First Hammer Star', [1], [Points_of_Ascendant], [4], [Points_of_Ascendant], rank=0,
             Physical_Damage=15/100, Armor=20)
hames = Star('Hammer', ' Second Hammer Star ', rank=1, Internal_Trauma_Damage=50/100, Defensive_Ability=15)
hamet = Star('Hammer', ' Third Hammer Star ', rank=2, Internal_Trauma_Damage=30/100, Physical_Damage=24/100,
             Armor_increase=6/100)
hammer = Constellation('Hammer', {Points_of_Ascendant.name: 4}, {Points_of_Ascendant.name: 1}, [hamef, hames, hamet])

bassaf = Star("Assassins_blade", "First Assasins blade Star", [1], [Points_of_Ascendant, Points_of_Order], [3, 2],
              [Points_of_Order], rank=0, Defensive_Ability=12)
bassas = Star("Assassins_blade", "Second Assasins blade Star", line=1, rank=1, Physical_Damage=15/100,
              Pierce_Damage=15/100)
bassat = Star("Assassins_blade", "Third Assasins blade Star", line=2, rank=1,  Pierce_Damage=15/100,
              Physical_Damage=15/100)
bassaft = Star("Assassins_blade", "Fourth Assasins blade Star", line=2, rank=2, Offensive_Ability=18)
assassin_mark = Star("Assassins_blade", "Assassins Mark", line=2, rank=3, Second_Duration=18,
                     Physical_Resistance=-32/100, Pierce_Resistance=-32/100)
assassins_blade = Constellation("Assassins_blade", {Points_of_Ascendant.name: bassaf.bonus_value[0],
                                Points_of_Order.name: bassaf.bonus_value[1]}, {Points_of_Order.name: bassaf.unlockr[0]},
                                [bassaf, bassas, bassat, bassaft, assassin_mark])

assaf = Star('Assassin', 'First Assassin Star', [6, 4], [Points_of_Ascendant, Points_of_Order], [1, 1],
             [Points_of_Ascendant, Points_of_Order], rank=0, Pierce_Damage=40/100, tier=2)
assas = Star('Assassin', ' Second Assassin Star ', rank=1, Cunning=20, Health=60)
assat = Star('Assassin', ' Third Assassin Star ', line=1, rank=2, Offensive_Ability=18, Defensive_Ability=10)
assaft = Star('Assassin', ' Fourth Assassin Star ', rank=2, Cunning=5/100, Bleeding_Resistance=10/100)
assaff = Star('Assassin', ' Fifth Assassin Star ', line=2, rank=3, Damage_to_Humans=8/100, Defensive_Ability=25,
              Poison_and_Acid_Resistance=10/100)
assast = Star('Assassin', ' Sixth Assassin Star ', line=3, rank=3, Pierce_Damage=[8, 50/100])
blades_of_wrath = Star('Assassin', 'Blades of Wrath', line=3, rank=4, Seconds_Skill_Recharge=2, Projectiles=16,
                       Weapon_Damage=20/100, Pierce_Damage=range(248, 288), Chance_to_pass_through_Enemies=100/100)
assassin = Constellation("Assassin", {Points_of_Ascendant.name: assaf.bonus_value[0], Points_of_Order.name:
                         assaf.bonus_value[1]}, {Points_of_Ascendant.name: assaf.unlockr[0],
                         Points_of_Order.name: assaf.unlockr[1]},
                         [assaf, assas, assat, assaft, assaff, assast, blades_of_wrath], tier=2)

dryaf = Star('Dryad', 'First Dryad Star', [1], [Points_of_Order], [3], [Points_of_Order],  rank=0, Physique=15,
             Energy=200, Poison_and_Acid_Resistance=10/100)
dryas = Star('Dryad', ' Second Dryad Star ', rank=1, Health=80, Energy_Regenerated_per_Second=1)
dryat = Star('Dryad', ' Third Dryad Star ', rank=2, Movement_Speed=3/100, Slow_Resistance=15/100)
dryaft = Star('Dryad', ' Fourth Dryad Star ', rank=3, Spirit=5/100, Physical_Resistance=4/100,
              Spirit_Requirement_for_Jewelry=10/100, Spirit_Requirement_for_Weapon=10/100)
dryads_blessing = Star('Dryad', "Dryads Blessing", rank=4, Seconds_Skill_Recharge=2.7, Second_Duration=10,
                       Health_Restored=[10/100, 598], Armor=70, Reduction_in_Poison_Duration=36/100,
                       Reduction_in_Bleeding_Duration=36/100)
dryad = Constellation('Dryad', {Points_of_Order.name: 3}, {Points_of_Order.name: 1},
                      [dryaf, dryas, dryat, dryaft, dryads_blessing])

eelf = Star('Eel', 'First Eel Star', [1], [Points_of_Primordial], [5], [Points_of_Primordial], rank=0,
            Defensive_Ability=12, Chance_to_Avoid_Melee_Attacks=2/100)
eels = Star('Eel', ' Second Eel Star ', rank=1, Chance_to_Avoid_Projectiles=2/100, Defensive_Ability=15)
eelt = Star('Eel', ' Third Eel Star ', rank=2, Defensive_Ability=20, Movement_Speed=6/100, Pierce_Resistance=10/100)
eel = Constellation("Eel", {Points_of_Primordial.name: eelf.bonus_value[0]},
                    {Points_of_Primordial.name: eelf.unlockr[0]}, [eelf, eels, eelt])

panthef = Star('Panther', 'First Panther Star', [1], [Points_of_Primordial, Points_of_Order], [3, 2], [Points_of_Order],
               rank=0, Offensive_Ability=12, pets_Offensive_Ability=2/100)
panthes = Star('Panther', ' Second Panther Star ', rank=1, Cunning=15, Spirit=15, pets_to_All_Damage=15/100)
panthet = Star('Panther', ' Third Panther Star ', rank=2, Offensive_Ability=16, Increases_Energy_Regeneration=15/100,
               pets_Offensive_Ability_perc=3/100)
pantheft = Star('Panther', ' Fourth Panther Star ', rank=3, Offensive_Ability=25, Crit_Damage=6/100,
                pets_Crit_Damage=5/100)
panther = Constellation("Panther", {Points_of_Primordial.name: panthef.bonus_value[0],
                        Points_of_Order.name: panthef.bonus_value[1]}, {Points_of_Order.name: panthef.unlockr[0]},
                        [panthef, panthes, panthet, pantheft])

staf = Star('Stag', 'First Stag Star', [1], [Points_of_Primordial, Points_of_Order], [3, 2], [Points_of_Order],
            rank=0, Physical_Damage=15/100, Bleeding_Damage=15/100)
stas = Star('Stag', ' Second Stag Star ', rank=1, Physique=15, Movement_Speed=5/100, Pierce_Resistance=10/100)
stat = Star('Stag', ' Third Stag Star ', rank=2, Health=80, Defensive_Ability=15, to_All_Retaliation_Damage=30/100)
staft = Star('Stag', ' Fourth Stag Star ', rank=3, Physical_Damage=24/100, Bleeding_Damage=24/100,
             Physical_Resistance=3/100)
stag = Constellation("Stag", {Points_of_Primordial.name: staf.bonus_value[0],
                     Points_of_Order.name: staf.bonus_value[1]}, {Points_of_Order.name: staf.unlockr[0]},
                     [staf, stas, stat, staft])

srattof = Star('Rattosh_Staff', 'First Rattosh Staff Star', [6, 3, 3], [Points_of_Primordial, Points_of_Order], [3, 2],
               [Points_of_Primordial, Points_of_Chaos, Points_of_Order], rank=0, Defensive_Ability=20,
               pets_Defensive_Ability=3/100, tier=2)
srattos = Star('Rattosh_Staff', ' Second Rattosh Staff Star ', rank=1, Aether_Resistance=15/100,
               pets_Aether_Resistance=15/100)
srattot = Star('Rattosh_Staff', ' Third Rattosh Staff Star ', line=1, rank=2, Aether_Damage=50/100,
               pets_to_All_Damage=50/100)
srattoft = Star('Rattosh_Staff', ' Fourth Rattosh Staff Star ', line=1, rank=3, Offensive_Ability=3/100,
                pets_Crit_Damage=6/100, pets_Offensive_Ability=3/100,)
srattoff = Star('Rattosh_Staff', ' Fifth Rattosh Staff Star ', line=2, rank=2, Health=150, pets_to_All_Damage=30/100)
srattost = Star('Rattosh_Staff', ' Sixth Rattosh Staff Star ', line=2, rank=3, Health=5/100, Vitality_Resistance=10/100,
                pets_Vitality_Resistance=10/100)
rattosh_staff = Constellation("Rattosh_Staff", {Points_of_Primordial.name: 3, Points_of_Chaos.name: 2},
                              {Points_of_Primordial.name: 6, Points_of_Chaos.name: 3, Points_of_Order.name: 3},
                              [srattof, srattos, srattot, srattoft, srattoff, srattost], tier=2)

widof = Star('Widow', 'First Widow Star', [6, 4], [Points_of_Primordial], [3], [Points_of_Eldritch,
             Points_of_Primordial], rank=0, Aether_Damage=40/100, tier=2)
widos = Star('Widow', ' Second Widow Star ', rank=1, Energy=5/100, Offensive_Ability=18)
widot = Star('Widow', ' Third Widow Star ', rank=2, Physique=15, Spirit=15, Aether_Damage=30/100)
widoft = Star('Widow', ' Fourth Widow Star ', rank=3, Vitality_Resistance=8/100, Aether_Resistance=18/100)
widoff = Star('Widow', ' Fifth Widow Star ', rank=4, Lightining_Damage=50/100, Aether_Damage=50/100,
              Offensive_Ability=2/100)
arcane_bomb = Star('Widow', 'Arcane Bomb', rank=5, Seconds_Skill_Recharge=2, Meter_Radius=1, Summon_Limit=6,
                   Arcane_Bomb_Attributes={'attr1': 'Lives for 24 Seconds attr', 'attr2': '7448 Health attr',
                                           'attr3': '300 Energy attr'},
                   Arcane_Mark={'skl1': '4 Second Duration skl',
                                'skl2': '5 Meter Radius skl', 'skl3': '120 Lightining Damage skl',
                                'skl4': '120 Aether Damage skl', 'skl5': '-95 Offensive Ability skl',
                                'skl6': '-35% Lightining Resistance skl',
                                'skl7': '-35% Aether Resistance skl'})
widow = Constellation("Widow", {Points_of_Primordial.name: widof.bonus_value[0]},
                      {Points_of_Eldritch.name: widof.unlockr[0], Points_of_Primordial.name: widof.unlockr[1]},
                      [widof, widos, widot, widoft, widoff, arcane_bomb], tier=2)

krakef = Star('Kraken', 'First Kraken Star', [5, 5], [Points_of_Primordial, Points_of_Chaos], [3, 2],
              [Points_of_Primordial, Points_of_Eldritch], rank=0, to_All_Damage=50/100, tier=2)
krakes = Star('Kraken', ' Second Kraken Star ', line=1, rank=1, Health=180, Attack_Speed=10/100, Casting_Speed=4/100)
kraket = Star('Kraken', ' Third Kraken Star ', line=2, rank=1, Health=180, Attack_Speed=10/100, Casting_Speed=4/100)
krakeft = Star('Kraken', ' Fourth Kraken Star ', line=3, rank=1, to_All_Damage=70/100, Movement_Speed=5/100)
krakeff = Star('Kraken', ' Fifth Kraken Star ', line=4, rank=1, Crit_Damage=15/100, Physical_Resistance=4/100)
kraken = Constellation("Kraken", {Points_of_Primordial.name: krakef.bonus_value[0],
                                  Points_of_Chaos.name: krakef.bonus_value[1]},
                       {Points_of_Primordial.name: krakef.unlockr[0], str(Points_of_Eldritch.name): krakef.unlockr[1]},
                       [krakef, krakes, kraket, krakeft, krakeff], tier=2)

wraif = Star('Wraith', 'First Wraith Star', [1], [Points_of_Primordial, Points_of_Ascendant], [3, 3],
             [Points_of_Primordial], rank=0, Lightining_Damage=15/100, Aether_Damage=15/100)
wrais = Star('Wraith', ' Second Wraith Star ', line=1, rank=1, Lightining_Damage=24/100, Aether_Damage=24/100,
             Damage_to_Undead=6/100)
wrait = Star('Wraith', ' Third Wraith Star ', line=2, rank=2, Spirit=15, Aether_Resistance=8/100,
             to_All_Retaliation_Damage=20/100)
wraift = Star('Wraith', ' Fourth Wraith Star ', line=3, rank=3, Offensive_Ability=24,
              Energy_Absorbed_From_Enemy_Spells=15/100, Lightining_Retaliation=range(1, 70))
wraith = Constellation("Wraith", {Points_of_Primordial.name: wraif.bonus_value[0],
                                  Points_of_Ascendant.name: wraif.bonus_value[1]},
                       {Points_of_Primordial.name: wraif.unlockr[0]}, [wraif, wrais, wrait, wraift])

tempef = Star('Tempest', 'First Tempest Star', [5, 5], [Points_of_Eldritch, Points_of_Primordial], [1, 1],
              [Points_of_Primordial, Points_of_Ascendant], rank=0, Lightining_Damage=40/100, tier=2)
tempes = Star('Tempest', ' Second Tempest Star ', rank=1, Lightining_Damage=range(1, 20), Physique=20)
tempet = Star('Tempest', ' Third Tempest Star ', rank=2, Lightining_Damage=50/100, Electrocute_Damage=50/100)
tempeft = Star('Tempest', ' Fourth Tempest Star ', rank=3, Offensive_Ability=20, Defensive_Ability=20,
               Lightining_Resistance=25/100)
tempeff = Star('Tempest', ' Fifth Tempest Star ', line=1, rank=4, Chance_of_250_Lightining_Damage=30/100,
               Movement_Speed=3/100, Reduced_Stun_Duration=15/100)
tempestc = Star('Tempest', ' Sixth Tempest Star ', line=2, rank=4, Electrocute_Damage=50/100, Offensive_Ability=20)
reckless_tempest = Star('Tempest', 'Reckless Tempest', line=2, rank=5, Seconds_Skill_Recharge=10, Seconds_Duration=6,
                        Meter_Target_Area=8, Target_Maximum=4, Lightining_Damage=range(65, 267), Electrocute_Damage=408,
                        Chance_to_Stun=[20/100, 0.7])
tempest = Constellation("Tempest", {Points_of_Eldritch.name: tempef.bonus_value[0],
                                    Points_of_Primordial.name: tempef.bonus_value[1]},
                        {Points_of_Primordial.name: tempef.unlockr[0], Points_of_Ascendant.name: tempef.unlockr[1]},
                        [tempef, tempes, tempet, tempeft, tempeff, tempestc, reckless_tempest], tier=2)

vultuf = Star('Vulture', 'First Vulture Star', [1], [Points_of_Chaos], [5], [Points_of_Chaos], rank=0, Cunning=15,
              Spirit=15)
vultus = Star('Vulture', ' Second Vulture Star ', rank=1, Bleeding_Resistance=15/100, Offensive_Ability=15,
              Life_Leech_Resistance=30/100)
vultut = Star('Vulture', ' Third Vulture Star ', line=1, rank=2, Cunning=5/100, Spirit=5/100, Offensive_Ability=10)
vultuft = Star('Vulture', ' Fourth Vulture Star ', line=2, rank=2, Vitality_Resistance=15/100, Chaos_Resistance=8/100,
               Offensive_Ability=15)
vultuff = Star('Vulture', ' Fifth Vulture Star ', line=3, rank=2, Health=80, Energy=200, Offensive_Ability=15)
vulture = Constellation("Vulture", {Points_of_Chaos.name: vultuf.bonus_value[0]},
                        {Points_of_Chaos.name: vultuf.unlockr[0]}, [vultuf, vultus, vultut, vultuft, vultuff])

fief = Star('Fiend', 'First Fiend Star', [1], [Points_of_Eldritch, Points_of_Chaos], [3, 2], [Points_of_Chaos], rank=0,
            Fire_Damage=15/100, Chaos_Damage=15/100)
fies = Star('Fiend', ' Second Fiend Star ', rank=1, Spirit=15, pets_Fire_Damage=25/100)
fiet = Star('Fiend', ' Third Fiend Star ', rank=2, Chaos_Resistance=8/100)
fieft = Star('Fiend', ' Fourth Fiend Star ', rank=3, Fire_Damage=24/100, Chaos_Damage=24/100, pets_Fire_Damage=40/100)
flame_torrent = Star('Fiend', 'Flame Torrent', rank=4, Seconds_Skill_Recharge=0.5, Meter_Radius=0.5,
                     Chance_to_pass_through_Enemies=100/100, Weapon_Damage=20/100, Fire_Damage=178, Chaos_Damage=126,
                     Burn_Damage=420)
fiend = Constellation("Fiend", {Points_of_Eldritch.name: fief.bonus_value[0],
                                Points_of_Chaos.name: fief.bonus_value[1]}, {Points_of_Chaos.name: fief.unlockr[0]},
                      [fief, fies, fiet, fieft, flame_torrent])

ghouf = Star('Ghoul', 'First Ghoul Star', [1], [Points_of_Chaos], [3], [Points_of_Chaos], rank=0, Physique=15,
             Defensive_Ability=8)
ghous = Star('Ghoul', ' Second Ghoul Star ', rank=1, Health=3/100, Health_Regenerated_Per_Second=6)
ghout = Star('Ghoul', ' Third Ghoul Star ', line=1, rank=2, Physique=15, Spirit=15, Defensive_Ability=15)
ghouft = Star('Ghoul', ' Fourth Ghoul Star ', line=2, rank=2, of_Attack_Damage_Converted_To_Health=4/100,
              Increases_Health_Regeneration=15/100)
ghoulish_hunger = Star('Ghoul', 'Ghoulish Hunger', line=2, rank=3, Seconds_Skill_Recharge=30, Seconds_Duration=5,
                       of_Attack_Damage_Converted_To_Health=80/100, Attack_Speed=22/100, Physical_Resistance=18/100)
ghoul = Constellation("Ghoul", {Points_of_Chaos.name: ghouf.bonus_value[0]},
                      {Points_of_Chaos.name: ghouf.unlockr[0]}, [ghouf, ghous, ghout, ghouft, ghoulish_hunger])


spidef = Star('Spider', 'First Spider Star', [1], [Points_of_Eldritch], [6], [Points_of_Eldritch], rank=0, Cunning=15,
              Spirit=15)
spides = Star('Spider', ' Second Spider Star ', line=1, rank=1, Cunning=3/100, Defensive_Ability=20)
spidet = Star('Spider', ' Third Spider Star ', line=2, rank=1, Defensive_Ability=20, Attack_Speed=5/100)
spideft = Star('Spider', ' Fourth Spider Star ', line=3, rank=1, Offensive_Ability=20, Casting_Speed=5/100)
spideff = Star('Spider', ' Fifth Spider Star ', line=4, rank=1, Spirit=3/100, Offensive_Ability=20)
spider = Constellation("Spider", {Points_of_Eldritch.name: spidef.bonus_value[0]},
                       {Points_of_Eldritch.name: spidef.unlockr[0]}, [spidef, spides, spidet, spideft, spideff])

ravef = Star('Raven', 'First Raven Star', [1], [Points_of_Eldritch], [5], [Points_of_Eldritch], rank=0, Spirit=15,
             pets_to_All_Damage=15/100)
raves = Star('Raven', ' Second Raven Star ', rank=1, Offensive_Ability=10, Energy_Regenerated_per_Second=1)
ravet = Star('Raven', ' Third Raven Star ', line=1, rank=2, Offensive_Ability=3/100, pets_Offensive_Ability=5/100)
raveft = Star('Raven', ' Fourth Raven Star ', line=2, rank=2, Offensive_Ability=15, pets_Lightining_Damage=[6, 60/100])
raven = Constellation("Raven", {Points_of_Eldritch.name: ravef.bonus_value[0]},
                      {Points_of_Eldritch.name: ravef.unlockr[0]}, [ravef, raves, ravet, raveft])

quif = Star('Quill', 'First Quill Star', [1], [Points_of_Eldritch, Points_of_Ascendant], [3, 3], [Points_of_Eldritch],
            rank=0, Elemental_Damage=15/100)
quis = Star('Quill', ' Second Quill Star ', rank=1, Aether_Resistance=8/100)
quitt = Star('Quill', ' Third Quill Star ', rank=2, Health=60, Energy=150)
quift = Star('Quill', ' Fourth Quill Star ', rank=3, Elemental_Damage=24/100, Energy=5/100, Defensive_Ability=2/100)
quill = Constellation("Quill", {Points_of_Eldritch.name: quif.bonus_value[0],
                                Points_of_Ascendant.name: quif.bonus_value[1]},
                      {Points_of_Eldritch.name: quif.unlockr[0]}, [quif, quis, quitt, quift])

lschof = Star("Scholars_Light", "First Scholars Light Star", [1], [Points_of_Eldritch], [4], [Points_of_Eldritch],
              rank=0, Elemental_Damage=15/100)
lschos = Star("Scholars_Light", "Second Scholars Light Star ", rank=1, Physique=15, Defensive_Ability=15,
              Elemental_Resistance=8/100)
lschot = Star("Scholars_Light", "Third Scholars Light Star ", rank=2, Elemental_Damage=24/100,
              Energy_Regenerated_per_Second=3, Aether_Resistance=8/100)
scholars_light = Constellation("Scholars_Light", {Points_of_Eldritch.name: lschof.bonus_value[0]},
                               {Points_of_Eldritch.name: lschof.unlockr[0]}, [lschof, lschos, lschot])

hawkf = Star("Hawk", "First Hawk Star", [1], [Points_of_Eldritch], [3], [Points_of_Eldritch], rank=0,
             Offensive_Ability=15)
hawks = Star("Hawk", "Second Hawk Star", rank=1, Crit_Damage=8/100, pets_Crit_Damage=4/100)
hawkt = Star("Hawk", "Third Hawk Star", rank=2, Offensive_Ability=3/100, Cunning_Requirement_for_Ranged_Weapons=10/100,
             pets_Offensive_Ability=2/100)
hawk = Constellation("Hawk", {Points_of_Eldritch.name: hawkf.bonus_value[0]},
                     {Points_of_Eldritch.name: hawkf.unlockr[0]}, [hawkf, hawks, hawkt])

owlf = Star("Owl", "First Owl Star", [1], [Points_of_Ascendant], [5], [Points_of_Ascendant], rank=0, Cunning=15,
            Spirit=15)
owls = Star("Owl", "Second Owl Star", rank=1, Elemental_Resistance=8/100, Energy_Cost=-5/100)
owlt = Star("Owl", "Third Owl Star", line=2, rank=2, Internal_Trauma_Damage=50/100, Bleeding_Damage=50/100,
            Burn_Damage=50/100, Frostburn_Damage=50/100, Electrocute_Damage=50/100, Poison_Damage=50/100,
            Vitality_Decay=50/100)
owlft = Star("Owl", "Fourth Owl Star", line=3, rank=2, to_All_Damage=30/100, Defensive_Ability=15,
             Reflected_Damage_Reduction=15/100)
owl = Constellation("Owl", {Points_of_Ascendant.name: owlf.bonus_value[0]},
                    {Points_of_Ascendant.name: owlf.unlockr[0]}, [owlf, owls, owlt, owlft])

harpyf = Star("Harpy", "First Harpy Star", [1], [Points_of_Ascendant], [5], [Points_of_Ascendant], Pierce_Damage=15/100,
              Cold_Damage=15/100, rank=0)
harpys = Star("Harpy", "Second Harpy Star", rank=1, Cunning=15, Energy_Regenerated_per_Second=1.5)
harpyt = Star("Harpy", "Third Harpy Star", rank=2, Offensive_Ability=24, Bleeding_Resistance=10/100)
harpyft = Star("Harpy", "Fourth Harpy Star", rank=2, Pierce_Damage=[24/100, range(4, 8)], Crit_Damage=3/100,
               Cold_Damage=24/100)
harpy = Constellation("Harpy", {Points_of_Ascendant.name: harpyf.bonus_value[0]},
                      {Points_of_Ascendant.name: harpyf.unlockr[0]}, [harpyf, harpys, harpyt, harpyft])

tarbuf = Star("Targo_the_Builder", "First Targo the Builder Star", [6, 4], [Points_of_Order], [1],
              [Points_of_Primordial, Points_of_Order], rank=0, Defensive_Ability=20, to_All_Retaliation_Damage=30/100,
              tier=2)
tarbus = Star("Targo_the_Builder", "Second Targo the Builder Star", rank=1, Health=5/100, Aether_Resistance=8/100)
tarbut = Star("Targo_the_Builder", "Third Targo the Builder Star", line=1, rank=2, Armor=5/100,
              Physical_Damage_Retaliation=100)
tarbuft = Star("Targo_the_Builder", "Fourth Targo the Builder Star", rank=2, Health=5/100, Chaos_Resistance=8/100)
tarbuff = Star("Targo_the_Builder", "Fifth Targo the Builder Star", line=2, rank=3, Health=300, Defensive_Ability=35,
               to_All_Retaliation_Damage=30/100,)
tarbust = Star("Targo_the_Builder", "Sixth Targo the Builder Star", line=3,  rank=3, Armor=5/100,
               Shield_Damage_Blocked=20/100)
shield_wall = Star("Targo_the_Builder", "Shield Wall", line=3, rank=4, Seconds_Skill_Recharge=8, Second_Duration=5,
                   Armor=35/100, Shield_Damage_Blocked=150/100, Physical_Damage_Retaliation=535)
targo_the_builder = Constellation("Targo_the_Builder", {Points_of_Order.name: tarbuf.bonus_value[0]},
                                  {Points_of_Primordial.name: tarbuf.unlockr[0],
                                   Points_of_Order.name: tarbuf.unlockr[1]},
                                  [tarbuf, tarbus, tarbut, tarbuft, tarbuff, tarbust, shield_wall], tier=2)

bnadaf = Star("Blades_of_Nadan", "First Blades of Nadaan Star", [10], [Points_of_Ascendant, Points_of_Order],
              [3, 2], [Points_of_Ascendant], rank=0, Chance_to_Avoid_Melee_Attacks=2/100,
              Chance_to_Avoid_Projectiles=2/100, tier=2)
bnadas = Star("Blades_of_Nadan", "Second Blades of Nadaan Star", rank=1, Pierce_Damage=40/100)
bnadat = Star("Blades_of_Nadan", "Third Blades of Nadaan Star", line=1, rank=2, Defensive_Ability=8, Attack_Speed=4/100)
bnadaft = Star("Blades_of_Nadan", "Fourth Blades of Nadaan Star", line=2, rank=2, Pierce_Damage=50/100)
bnadaff = Star("Blades_of_Nadan", "Fifth Blades of Nadaan Star", line=3, rank=2, Defensive_Ability=8,
               Attack_Speed=4/100)
bnadast = Star("Blades_of_Nadan", "Sixth Blades of Nadaan Star", line=4, rank=2, Pierce_Damage=8,
               Increases_Armor_Piercing=100/100)
blades_of_nadan = Constellation("Blades_of_Nadan", {Points_of_Ascendant.name: bnadaf.bonus_value[0],
                                                    Points_of_Order.name: bnadaf.bonus_value[1]},
                                {Points_of_Ascendant.name: bnadaf.unlockr[0]},
                                [bnadaf, bnadas, bnadat, bnadaft, bnadaff, bnadast], tier=2)

uscaf = Star("Schales_of_Ulcana", "First Schales of Ulcana Star", [8], [Points_of_Order], [2], [Points_of_Order],
             rank=0, Health=150, Energy=300, tier=2)
uscas = Star("Schales_of_Ulcana", "Second Schales of Ulcana Star", rank=1, Health=4/100, Movement_Speed=4/100)
uscat = Star("Schales_of_Ulcana", "Third Schales of Ulcana Star", line=2, rank=2, Energy_Regenerated_per_Second=3,
             Increases_Energy_Regeneration=33/100)
uscaft = Star("Schales_of_Ulcana", "Fourth Schales of Ulcana Star", line=2, rank=3,
              of_Attack_Damage_Converted_To_Health=3/100, Health_Regenerated_Per_Second=30,
              Increases_Health_Regeneration=33/100)
uscaff = Star("Schales_of_Ulcana", "Fifth Schales of Ulcana Star", line=1, rank=2, Physique=20, Defensive_Ability=30)
tip_scales = Star("Schales_of_Ulcana", "Tip the Scales", line=1, rank=3, Seconds_Skill_Recharge=1, Weapon_Damage=33/100,
                  Vitality_Damage=310, of_Attack_Damage_Converted_To_Health=132/100, Energy_Leech=400,
                  Reduced_target_Resistances=20)
schales_of_ulcana = Constellation("Schales_of_Ulcana", {Points_of_Order.name: uscaf.bonus_value[0]},
                                  {Points_of_Order.name: uscaf.unlockr[0]},
                                  [uscaf, uscas, uscat, uscaft, uscaff, tip_scales], tier=2)

wsolef = Star("Solemn_Watcher", "First Solemn Watcher Star", [10], [Points_of_Primordial, Points_of_Order], [3, 2],
              [Points_of_Primordial], rank=0, Physique=20, tier=2)
wsoles = Star("Solemn_Watcher", "Second Solemn Watcher Star", rank=1, Cold_Resistance=25/100, Armor=40)
wsolet = Star("Solemn_Watcher", "Third Solemn Watcher Star", rank=2, Pierce_Resistance=18/100, Armor=40)
wsoleft = Star("Solemn_Watcher", "Fourth Solemn Watcher Star", rank=3, Defensive_Ability=30, Physique=3/100)
wsoleff = Star("Solemn_Watcher", "Fifth Solemn Watcher Star", rank=4, Defensive_Ability=4/100,
               Reflected_Damage_Reduction=20/100)
solemn_watcher = Constellation('Solemn_Watcher', {Points_of_Primordial.name: 3, Points_of_Order.name: 2},
                               {Points_of_Primordial.name: 10}, [wsolef, wsoles, wsolet, wsoleft, wsoleff], tier=2)

lotuf = Star("Lotus", "First Lotus Star", [1], [Points_of_Eldritch, Points_of_Order], [3, 2], [Points_of_Order], rank=0,
             Health=30, Energy=100)
lotusc = Star("Lotus", "Second Lotus Star", line=1, rank=1, Physical_Resistance=3/100, Healing_Effects_Increased=10/100)
lotut = Star("Lotus", "Third Lotus Star", line=2, rank=1, Health=80, Energy=4/100, Vitality_Resistance=8/100)
lotuft = Star("Lotus", "Fourth Lotus Star", line=3, rank=1, Energy_Regenerated_per_Second=1,
              Increases_Energy_Regeneration=15/100)
lotus = Constellation("Lotus", {Points_of_Eldritch.name: lotuf.bonus_value[0],
                                Points_of_Order.name: lotuf.bonus_value[1]}, {Points_of_Order.name: lotuf.unlockr[0]},
                      [lotuf, lotusc, lotut, lotuft])

bdiref = Star("Dire_Bear", "First Dire Bear Star", [5, 5], [Points_of_Primordial, Points_of_Ascendant], [1, 1],
              [Points_of_Primordial, Points_of_Ascendant], rank=0, Physical_Damage=40/100, tier=2)
bdires = Star("Dire_Bear", "Second Dire Bear Star", rank=1, Physique=20, Cunning=20, Defensive_Ability=15)
bdiret = Star("Dire_Bear", "Third Dire Bear Star", rank=2, Physical_Damage=50/100, Armor=60)
bdireft = Star("Dire_Bear", "Fourth Dire Bear Star", rank=3, Health=5/100, Reduced_Stun_Duration=15/100,
               Reduced_Freeze_Duration=15/100)
bdireff = Star("Dire_Bear", "Fifth Dire Bear Star", line=1, rank=4, Defensive_Ability=2/100, Armor=80)
maul = Star("Dire_Bear", "maul", line=2, rank=4, Seconds_Skill_Recharge=1, Seconds_Duration=3, Meter_Radius=4,
            Physical_Damage=305, Increases_Armor=-35/100, of_Attack_Damage_Converted_To_Health=40/100)
dire_bear = Constellation('Dire_Bear', {Points_of_Primordial.name: 1, Points_of_Ascendant.name: 1},
                          {Points_of_Primordial.name: 5, Points_of_Ascendant.name: 5},
                          [bdiref, bdires, bdiret, bdireft, bdireff, maul], tier=2)

amatof = Star("Amatok_the_Spirit_of_Winter", "First Amatok the Spirit of Winter Star", [6, 4],
              [Points_of_Primordial, Points_of_Eldritch], [1, 1], [Points_of_Primordial, Points_of_Eldritch],
              rank=0, Cold_Damage=40/100, tier=2)
amatos = Star("Amatok_the_Spirit_of_Winter", "Second Amatok the Spirit of Winter Star", rank=1, Health=4/100,
              Defensive_Ability=15)
amatot = Star("Amatok_the_Spirit_of_Winter", "Third Amatok the Spirit of Winter Star", line=2, rank=2,
              Defensive_Ability=30, Cold_Resistance=25/100)
amatoft = Star("Amatok_the_Spirit_of_Winter", "Fourth Amatok the Spirit of Winter Star", line=1, rank=2,
               Cold_Damage=50/100, Frostburn_Damage=50/100, Health=100)
amatoff = Star("Amatok_the_Spirit_of_Winter", "Fifth Amatok the Spirit of Winter Star", line=1, rank=3,
               Frostburn_Damage=[36, 100/100], Cold_Damage=50/100)
amatost = Star("Amatok_the_Spirit_of_Winter", "Sixth Amatok the Spirit of Winter Star", line=3, rank=2,
               Offensive_Ability=25, Frostburn_Damage=50/100)
blizzard = Star("Amatok_the_Spirit_of_Winter", "Blizzard", line=3, rank=3, Seconds_Skill_Recharge=3.2,
                Meter_Radius=2, Meter_Target_Area=6.5, Weapon_Damage=16/100, Cold_Damage=range(315, 392),
                Frostburn_Damage=360, Chance_to_Freeze_Target=50/100, Slower_target_Movement=70/100)
amatok_the_spirit_of_winter = Constellation("Amatok_the_Spirit_of_Winter",
                                            {Points_of_Primordial.name: amatof.bonus_value[0],
                                             Points_of_Eldritch.name: amatof.bonus_value[1]},
                                            {Points_of_Primordial.name: amatof.unlockr[0],
                                             Points_of_Eldritch.name: amatof.unlockr[1]},
                                            [amatof, amatos, amatot, amatoft, amatoff, amatost, blizzard], tier=2)

hspeaf = Star("Spear_of_The_Heavens", "First Spear of The Heavens Star", [20, 7], ['None'], [0], [Points_of_Primordial,
              Points_of_Chaos], rank=0, Lightining_Damage=80/100, Offensive_Ability=20, tier=3)
hspeas = Star("Spear_of_The_Heavens", "Second Spear of The Heavens Star", rank=1, Aether_Damage=80/100,
              Offensive_Ability=20)
hspeat = Star("Spear_of_The_Heavens", "Third Spear of The Heavens Star", rank=2, Offensive_Ability=5/100,
              Aether_Resistance=15/100)
hspeaft = Star("Spear_of_The_Heavens", "Fourth Spear of The Heavens Star", rank=3, Crit_Damage=5/100,
               Lightining_Resistance=20/100, Aether_Damage=10)
hspeaff = Star("Spear_of_The_Heavens", "Fifth Spear of The Heavens Star", rank=4, Lightining_Damage=100/100,
               Aether_Damage=100/100, Maximum_Lightining_Resistance=3/100)
heavens_spear = Star("Spear_of_The_Heavens", "Spear of The Heavens", rank=5, Seconds_Skill_Recharge=1,
                     Meter_Target_Area=0.5, Meter_Radius=2.4, Weapon_Damage=60/100, Lightining_Damage=range(175, 280),
                     Aether_Damage=294, Electrocute_Damage=236, Chance_to_Stun=1)
spear_of_the_heavens = Constellation("Spear_of_The_Heavens", [], {str(Points_of_Primordial.name): hspeaf.unlockr[0],
                                     str(Points_of_Chaos.name): hspeaf.unlockr[1]},
                                     [hspeaf, hspeas, hspeat, hspeaft, hspeaff, heavens_spear], tier=3)

wmessef = Star("Messenger_of_War", "First Messenger of War Star", [7, 3], [Points_of_Primordial, Points_of_Chaos],
               [3, 2], [Points_of_Primordial, Points_of_Ascendant], rank=0, Fire_Retaliation=90,
               to_All_Retaliation_Damage=30/100, tier=2)
wmesses = Star("Messenger_of_War", "Second Messenger of War Star", rank=1, Physique=20, Offensive_Ability=20,
               Movement_Speed=5/100)
wmesset = Star("Messenger_of_War", "Third Messenger of War Star", line=1, rank=2, Offensive_Ability=25,
               to_All_Retaliation_Damage=50/100)
wmesseft = Star("Messenger_of_War", "Fourth Messenger of War Star", line=1, rank=3, Armor=12/100, Fire_Retaliation=120)
wmesseff = Star("Messenger_of_War", "Fifth Messenger of War Star", line=2, rank=2, Elemental_Resistance=15/100,
                Fire_Retaliation=120)
war_messenger = Star("Messenger_of_War", "Messenger of War", line=2, rank=3, Seconds_Skill_Recharge=15,
                     Second_Duration=8, Movement_Speed=30/100, Slow_Resistance=70/100, Fire_Retaliation=780,
                     to_All_Retaliation_Damage=150/100)
messenger_of_war = Constellation("Messenger_of_War", {Points_of_Primordial.name: wmessef.bonus_value[0],
                                                      Points_of_Chaos.name: wmessef.bonus_value[1]},
                                 {Points_of_Primordial.name: wmessef.unlockr[0],
                                  Points_of_Ascendant.name: wmessef.unlockr[1]},
                                 [wmessef, wmesses, wmesset, wmesseft, wmesseff, war_messenger], tier=2)

dchariof = Star("Chariot_of_The_Dead", "First Chariot of The Dead Star", [5, 5], [Points_of_Eldritch, Points_of_Chaos],
                [3, 2], [Points_of_Ascendant, Points_of_Eldritch], rank=0, Physique=20, Cunning=20, tier=2)
dcharios = Star("Chariot_of_The_Dead", "Second Chariot of The Dead Star", rank=1, Offensive_Ability=15,
                Slow_Resistance=10/100)
dcharioft = Star("Chariot_of_The_Dead", "Fourth Chariot of The Dead Star", rank=2, Cunning=25, Health=100)
dchariot = Star("Chariot_of_The_Dead", "Third Chariot of The Dead Star", line=1, rank=2, Vitality_Resistance=16/100,
                Reduced_Stun_Duration=15/100)
dcharioff = Star("Chariot_of_The_Dead", "Fifth Chariot of The Dead Star", line=2, rank=3, Offensive_Ability=25,
                 Slow_Resistance=15/100)
dchariost = Star("Chariot_of_The_Dead", "Sixth Chariot of The Dead Star", line=2, rank=4, Offensive_Ability=[15, 4/100])
wayward_soul = Star("Chariot_of_The_Dead", "Wayward Soul", line=2, rank=5, Seconds_Skill_Recharge=18,
                    Seconds_Duration=7, Health_Restored=[12/100, 1550], Defensive_Ability=120, Armor=150)
chariot_of_the_dead = Constellation("Chariot_of_The_Dead", {Points_of_Eldritch.name: dchariof.bonus_value[0],
                                                            Points_of_Chaos.name: dchariof.bonus_value[1]},
                                    {Points_of_Ascendant.name: dchariof.unlockr[0],
                                     Points_of_Eldritch.name: dchariof.unlockr[1]},
                                    [dchariof, dcharios, dchariot, dcharioft, dcharioff, dchariost, wayward_soul],
                                    tier=2)

mantif = Star("Mantis", "First Mantis Star", [1], [Points_of_Ascendant, Points_of_Chaos], [3, 2],
              [Points_of_Chaos], rank=0, Pierce_Damage=15/100, Armor=20)
mantisc = Star("Mantis", "Second Mantis Star", rank=1, Elemental_Resistance=10/100, Defensive_Ability=10)
mantit = Star("Mantis", "Third Mantis Star", rank=2, Health=80, Energy_Regenerated_per_Second=1.5)
mantift = Star("Mantis", "Fourth Mantis Star", rank=3, Pierce_Damage=[5, 24/100], Physical_Resistance=3/100)
mantis = Constellation("Mantis", {Points_of_Ascendant.name: 3, Points_of_Chaos.name: 2}, {Points_of_Chaos.name: 1},
                       [mantif, mantisc, mantit, mantift])

wsolaef = Star("Solaels_Witchblade", "First Solaels Witchblade Star", [6, 4], [Points_of_Eldritch, Points_of_Chaos],
               [1, 1], [Points_of_Eldritch, Points_of_Chaos], rank=0, Chaos_Damage=40/100, tier=2)
wsolaes = Star("Solaels_Witchblade", "Second Solaels Witchblade Star", rank=1, Physique=15, Spirit=15,
               Offensive_Ability=10)
wsolaet = Star("Solaels_Witchblade", "Third Solaels Witchblade Star", rank=2, Fire_Damage=30/100, Chaos_Damage=30/100,
               Defensive_Ability=10)
wsolaeft = Star("Solaels_Witchblade", "Fourth Solaels Witchblade Star", rank=3, Fire_Damage=50/100,
                Chaos_Damage=50/100, Defensive_Ability=15)
eldritch_fire = Star("Solaels_Witchblade", "Eldritch Fire", rank=4, Seconds_Skill_Recharge=1, Seconds_Duration=4,
                     Fire_Damage=120, Chaos_Damage=120, Movement_Speed=-36/100, Fire_Resistance=-23/100,
                     Chaos_Resistance=-35/100)
solaels_witchblade = Constellation("Solaels_Witchblade", {Points_of_Eldritch.name: wsolaef.bonus_value[0],
                                                          Points_of_Chaos.name: wsolaef.bonus_value[1]},
                                   {Points_of_Eldritch.name: wsolaef.unlockr[0],
                                    Points_of_Chaos.name: wsolaef.unlockr[1]},
                                   [wsolaef, wsolaes, wsolaet, wsolaeft, eldritch_fire], tier=2)

bersef = Star("Berserker", "First Berserker Star", [5, 5], [Points_of_Eldritch, Points_of_Chaos], [3, 2],
              [Points_of_Ascendant, Points_of_Eldritch], rank=0, Health=200, Offensive_Ability=20, tier=2)
berses = Star("Berserker", "Second Berserker Star", line=3, rank=1, Physical_Resistance=3/100, Pierce_Resistance=15/100)
berset = Star("Berserker", "Third Berserker Star", line=2, rank=1, Physical_Damage=50/100, Bleeding_Damage=50/100,
              Reduced_Stun_Duration=15/100)
berseft = Star("Berserker", "Fourth Berserker Star", line=2, rank=2, Bleeding_Damage=[60, 50/100])
berseff = Star("Berserker", "Fifth Berserker Star", line=1, rank=1, Physical_Damage=50/100, Bleeding_Damage=50/100,
               Reduced_Freeze_Duration=15/100)
bersest = Star("Berserker", "Sixth Berserker Star", line=1, rank=2, Crit_Damage=5/100, Offensive_Ability=50)
berserker = Constellation("Berserker", {Points_of_Eldritch.name: bersef.bonus_value[0],
                                        Points_of_Chaos.name: bersef.bonus_value[1]},
                          {Points_of_Ascendant.name: bersef.unlockr[0], Points_of_Eldritch.name: bersef.unlockr[1]},
                          [bersef, berses, berset, berseft, berseff, bersest], tier=2)

bysmief = Star("Bysmiels_Bonds", "First Bysmiels Bonds Star", [6, 4], [Points_of_Eldritch], [3],
               [Points_of_Eldritch, Points_of_Chaos], rank=0, Offensive_Ability=15, pets_to_All_Damage=30/100, tier=2)
bysmies = Star("Bysmiels_Bonds", "Second Bysmiels Bonds Star", rank=1, Physique=15, Casting_Speed=5/100,
               pets_Total_Speed=8/100)
bysmiet = Star("Bysmiels_Bonds", "Third Bysmiels Bonds Star", rank=2, Vitality_Resistance=15/100,
               pets_Vitality_Resistance=20/100)
bysmieft = Star("Bysmiels_Bonds", "Fourth Bysmiels Bonds Star", rank=3, to_All_Damage=30/100, pets_to_All_Damage=40/100,
                pets_Health=10/100)
bysmiels_command = Star("Bysmiels_Bonds", "Bysmiels Command", rank=4, Seconds_Skill_Recharge=30, Summon_Limit=1,
                        Eldritch_Hound_Attributes={'attr1': 'Lives for 20 Seconds attr', 'attr2': '25691 Health attr',
                                                   'attr3': '1883 Energy attr'},
                        Eldritch_Hound_Abilities={'abl1': "155% to All Damage abl", 'abl2': '38% Crit Damage abl',
                                                  'abl3': '124% Health abl',
                                                  'abl4': '185% Increases Energy Regeneration abl'},
                        Tooth_and_Claws={'skl1': '83 - 130 Physical Damage skl', 'skl2': '112 - 150 Acid Damage skl',
                                         'skl3': '-180 Offensive Ability skl',
                                         'skl4': '25 Reduced_target_Resistances skl'})
bysmiels_bonds = Constellation("Bysmiels_Bonds", {Points_of_Eldritch.name: bysmief.bonus_value[0]},
                               {Points_of_Eldritch.name: bysmief.unlockr[0], Points_of_Chaos.name: bysmief.unlockr[1]},
                               [bysmief, bysmies, bysmiet, bysmieft, bysmiels_command], tier=2)

foxf = Star("Fox", "First Fox Star", [1], [Points_of_Eldritch], [5], [Points_of_Eldritch], rank=0, Cunning=15,
            Spirit=15)
foxs = Star("Fox", "Second Fox Star", rank=1, Bleeding_Damage=[24, 24/100])
foxt = Star("Fox", "Third Fox Star", rank=2, Cunning=25, Bleeding_Resistance=8/100)
foxft = Star("Fox", "Fourth Fox Star", rank=3, Bleeding_Damage=[36, 50/100], of_Attack_Damage_Converted_To_Health=4/100)
fox = Constellation("Fox", {Points_of_Eldritch.name: 5}, {str(Points_of_Eldritch.name): 1}, [foxf, foxs, foxt, foxft])

manticof = Star("Manticore", "First Manticore Star", [6, 4], [Points_of_Ascendant, Points_of_Eldritch], [1, 1],
                [Points_of_Eldritch, Points_of_Chaos], rank=0, Offensive_Ability=15, tier=2)
manticos = Star("Manticore", "Second Manticore Star", rank=1, Acid_Damage=50/100, Poison_Damage=50/100,
                pets_Poison_Damage=60/100)
manticot = Star("Manticore", "Third Manticore Star", rank=2, Health=5/100, pets_Health=5/100)
manticoft = Star("Manticore", "Fourth Manticore Star", line=1, rank=3, Physical_Resistance=4/100, Offensive_Ability=20,
                 Poison_and_Acid_Resistance=10/100, pets_Offensive_Ability=4/100)
manticoff = Star("Manticore", "Fifth Manticore Star", line=2, rank=3, Poison_Damage=[40, 40/100], Acid_Damage=40/100)
acid_spray = Star("Manticore", "Acid Spray", line=2, rank=4, Seconds_Skill_Recharge=1, Meter_Radius=4, Acid_Damage=217,
                  Poison_Damage=200, Reduced_target_Resistances=28)
manticore = Constellation("Manticore", {Points_of_Ascendant.name: 1, Points_of_Eldritch.name: 1},
                          {Points_of_Eldritch.name: 6, str(Points_of_Chaos.name): 4},
                          [manticof, manticos, manticot, manticoft, manticoff, acid_spray], tier=2)

sharvef = Star("Harvestmans_Scythe", "First Harvestmans Scythe Star", [5, 3, 3],
               [Points_of_Primordial, Points_of_Ascendant], [3, 3],
               [Points_of_Primordial, Points_of_Ascendant, Points_of_Order], rank=0, Energy_Regenerated_per_Second=2,
               Movement_Speed=3/100, tier=2)
sharves = Star("Harvestmans_Scythe", "Second Harvestmans Scythe Star", rank=1, Health=200, Energy=200,
               Movement_Speed=3/100)
sharvet = Star("Harvestmans_Scythe", "Third Harvestmans Scythe Star", rank=2, Physique=4/100,
               Healing_Effects_Increased=6/100)
sharveft = Star("Harvestmans_Scythe", "Fourth Harvestmans Scythe Star", rank=3, Cunning=4/100, Spirit=4/100)
sharveff = Star("Harvestmans_Scythe", "Fifth Harvestmans Scythe Star", rank=4, Defensive_Ability=3/100,
                Increases_Health_Regeneration=30/100, Increases_Energy_Regeneration=30/100)
sharvest = Star("Harvestmans_Scythe", "Sixth Harvestmans Scythe Star", rank=4, Health=5/100, Energy=5/100,
                Health_Regenerated_Per_Second=60, Energy_Regenerated_per_Second=3)
harvestmans_scythe = Constellation("Harvestmans_Scythe", {Points_of_Primordial.name: 3, Points_of_Ascendant.name: 3},
                                   {Points_of_Primordial.name: 5, str(Points_of_Ascendant.name): 3,
                                    Points_of_Order.name: 3}, [sharvef, sharves, sharvet, sharveft, sharveff, sharvest],
                                   tier=2)

ethrof = Star("Empty_Throne", "First Empty Throne Star", [1], [Points_of_Ascendant], [5], [Points_of_Ascendant], rank=0,
              Defensive_Ability=12, Slow_Resistance=10/100)
ethros = Star("Empty_Throne", "Second Empty Throne Star", rank=1, Defensive_Ability=20, Pierce_Resistance=8/100,
              pets_Pierce_Resistance=8/100)
ethrot = Star("Empty_Throne", "Third Empty Throne Star", line=1, rank=2, Aether_Resistance=10/100,
              Reduced_Freeze_Duration=22/100, pets_Aether_Resistance=10/100, pets_Reduced_Freeze_Duration=22/100)
ethroft = Star("Empty_Throne", "Fourth Empty Throne Star", line=2, rank=2, Chaos_Resistance=10/100,
               pets_Chaos_Resistance=10/100, Reduced_Stun_Duration=22/100, pets_Reduced_Stun_Duration=22/100)
empty_throne = Constellation("Empty_Throne", {Points_of_Ascendant.name: 5}, {Points_of_Ascendant.name: 1},
                             [ethrof, ethros, ethrot, ethroft])

rcrof = Star("Rhowans_Crown", "First Rhowans Crown Star", [6, 4], [Points_of_Eldritch, Points_of_Ascendant], [1, 1],
             [Points_of_Eldritch, Points_of_Ascendant], rank=0, Elemental_Damage=40/100, Burn_Damage=60/100,
             Electrocute_Damage=60/100, Frostburn_Damage=60/100, Chaos_Resistance=8/100, tier=2)
rcros = Star("Rhowans_Crown", "Second Rhowans Crown Star", rank=1, Spirit=20, Defensive_Ability=20,
             pets_Elemental_Damage=40/100)
rcrot = Star("Rhowans_Crown", "Third Rhowans Crown Star", rank=3, Elemental_Resistance=18/100,
             pets_Elemental_Resistance=10/100)
rcroft = Star("Rhowans_Crown", "Fourth Rhowans Crown Star", rank=4, Elemental_Damage=[range(6, 9), 30/100])
elemental_storm = Star("Rhowans_Crown", "Elemental Storm", rank=2, Seconds_Skill_Recharge=1.5, Seconds_Duration=5,
                       Meter_Radius=3.5, Elemental_Damage=132, Burn_Damage=156, Frostburn_Damage=156,
                       Electrocute_Damage=156, Reduced_target_Elemental_Resistances=32)
rhowans_crown = Constellation("Rhowans_Crown", {Points_of_Eldritch.name: 1, Points_of_Ascendant.name: 1},
                              {Points_of_Eldritch.name: 6, str(Points_of_Eldritch.name): 4},
                              [rcrof, rcros, elemental_storm, rcrot, rcroft], tier=2)

toadf = Star("Toad", "First Toad Star", [1], [Points_of_Ascendant, Points_of_Eldritch], [3, 3], [Points_of_Ascendant],
             rank=0, Vitality_Resistance=8/100)
toads = Star("Toad", "Second Toad Star", rank=1, Spirit=15, Offensive_Ability=10, pets_Offensive_Ability=3/100)
toadt = Star("Toad", "Third Toad Star", rank=2, of_Attack_Damage_Converted_To_Health=3/100, Health=60,
             pets_of_Attack_Damage_Converted_To_Health=4/100)
toadft = Star("Toad", "Fourth Toad Star", rank=3, Vitality_Damage=24/100, Aether_Damage=24/100, Damage_to_Beasts=6/100,
              pets_Offensive_Ability=3/100)
toad = Constellation("Toad", {Points_of_Ascendant.name: 3, Points_of_Eldritch.name: 3},
                     {Points_of_Ascendant.name: 1}, [toadf, toads, toadt, toadft])

typhof = Star("Typhos_The_Jailor_of_Souls", "First Typhos The Jailor of Souls Star", [6, 3, 3], [Points_of_Ascendant,
                                                                                                 Points_of_Order],
              [3, 2], [Points_of_Ascendant, Points_of_Order, Points_of_Chaos], rank=0, Offensive_Ability=20,
              pets_Offensive_Ability=3/100, tier=2)
typhos = Star("Typhos_The_Jailor_of_Souls", "Second Typhos The Jailor of Souls Star", rank=1, Defensive_Ability=20,
              pets_Defensive_Ability=3/100)
typhot = Star("Typhos_The_Jailor_of_Souls", "Third Typhos The Jailor of Souls Star", rank=2,
              Poison_and_Acid_Resistance=15/100, Bleeding_Resistance=15/100, pets_Poison_and_Acid_Resistance=15/100,
              pets_Bleeding_Resistance=15/100)
typhoft = Star("Typhos_The_Jailor_of_Souls", "Fourth Typhos The Jailor of Souls Star", line=1, rank=3,
               Physical_Resistance=4/100, pets_Total_Speed=6/100, pets_Physical_Resistance=10/100,
               pets_Reduced_Stun_Duration=50/100, pets_Reduced_Mind_Control_Seconds_Duration=50/100)
typhoff = Star("Typhos_The_Jailor_of_Souls", "Fifth Typhos The Jailor of Souls Star", line=2, rank=3, Health=5/100,
               Offensive_Ability=20, pets_Offensive_Ability=3/100)
typhost = Star("Typhos_The_Jailor_of_Souls", "Sixth Typhos The Jailor of Souls Star", line=2, rank=4,
               Crit_Damage=10/100, pets_Crit_Damage=12/100)
typhos_the_jailor_of_souls = Constellation("Typhos_The_Jailor_of_Souls", {Points_of_Ascendant.name: 3,
                                                                          Points_of_Order.name: 2},
                                           {Points_of_Ascendant.name: 6, str(Points_of_Order.name): 3,
                                            Points_of_Chaos.name: 3},
                                           [typhof, typhos, typhot, typhoft, typhoff, typhost], tier=2)

ulzaaf = Star("Ulzaad_Herald_of_Korvak", "First Ulzaad Herald of Korvak Star", [8, 6],
              [Points_of_Eldritch, Points_of_Ascendant], [2, 2], [Points_of_Ascendant, Points_of_Primordial], rank=0,
              Physical_Damage=40/100, tier=2)
ulzaas = Star("Ulzaad_Herald_of_Korvak", "Second Ulzaad Herald of Korvak Star", rank=1, Defensive_Ability=10,
              Cold_Resistance=15/100, Poison_and_Acid_Resistance=15/100)
ulzaat = Star("Ulzaad_Herald_of_Korvak", "Third Ulzaad Herald of Korvak Star", line=2, rank=2, Health=80,
              Chaos_Resistance=10/100)
ulzaaft = Star("Ulzaad_Herald_of_Korvak", "Fourth Ulzaad Herald of Korvak Star", line=1, rank=2, Health=80,
               Aether_Resistance=10/100)
ulzaaff = Star("Ulzaad_Herald_of_Korvak", "Fifth Ulzaad Herald of Korvak Star", line=3, rank=2,
               Physical_Damage=[range(6, 8), 50/100], Internal_Trauma_Damage=50/100)
ulzaads_decree = Star("Ulzaad_Herald_of_Korvak", "Ulzaads Decree", line=3, rank=3, Seconds_Skill_Recharge=22,
                      Second_Duration=10, Physical_Damage=[range(42, 45), 200/100], Internal_Trauma_Damage=200/100,
                      Armor=150, Physical_Damage_Retaliation=range(205, 450), Pierce_Damage=200/100)
ulzaad_herald_of_korvak = Constellation("Ulzaad_Herald_of_Korvak",
                                        {Points_of_Eldritch.name: 2, Points_of_Ascendant.name: 2},
                                        {Points_of_Ascendant.name: 8, Points_of_Primordial.name: 6},
                                        [ulzaaf, ulzaas, ulzaat, ulzaaft, ulzaaff, ulzaads_decree], tier=2)

usoldief = Star("Unknown_Soldier", "First Unknown Soldier Star", [15, 8], [Points_of_Ascendant, Points_of_Order], [0],
                [Points_of_Ascendant, Points_of_Order], rank=0, Pierce_Damage=80/100, Offensive_Ability=15, tier=3)
usoldies = Star("Unknown_Soldier", "Second Unknown Soldier Star", rank=1, Bleeding_Damage=[54, 80/100])
usoldiet = Star("Unknown_Soldier", "Third Unknown Soldier Star", line=1, rank=2, Health=280, Attack_Speed=5/100)
usoldieft = Star("Unknown_Soldier", "Fourth Unknown Soldier Star", line=2, rank=2, Pierce_Damage=100/100,
                 Bleeding_Damage=100/100)
usoldieff = Star("Unknown_Soldier", "Fifth Unknown Soldier Star", line=2, rank=3, Health=4/100, Offensive_Ability=40)
usoldiest = Star("Unknown_Soldier", "Sixth Unknown Soldier Star", line=2, rank=4, Pierce_Damage=9, Crit_Damage=12/100)
unknown_soldier_skill = Star("Unknown_Soldier", "Unknown Soldier", line=2, rank=5, Seconds_Skill_Recharge=6,
                             Summon_Limit=3,
                             Living_Shadow_Attributes={'attr1': 'Lives for 24 Seconds attr',
                                                       'attr2': 'Invincible attr', 'attr3': '6526 Energy attr'},
                             Shadow_Strike={'skl1': '205 - 273 Piercing Damage skl',
                                            'skl2': '25% of Attack Damage Converted to Health skl',
                                            'skl3': '163 Bleeding Damage skl', 'skl4': '+100% Movement Speed skl'},
                             Shadow_Blades={'acv1': '172 - 226 Piercing Damage acv',
                                            'acv2': '25% of Attack Damage Converted to Health acv',
                                            'acv3': '298 Bleeding Damage acv'})
unknown_soldier = Constellation("Unknown_Soldier", [], {Points_of_Ascendant.name: 15, Points_of_Order.name: 8},
                                [usoldief, usoldies, usoldiet, usoldieft, usoldieff, usoldiest, unknown_soldier_skill],
                                tier=3)

barhaf = Star("Bards_Harp", "First Bards Harp Star", [6, 6, 3], [Points_of_Primordial, Points_of_Order], [2, 2],
              [Points_of_Primordial, Points_of_Ascendant, Points_of_Order], rank=0, Health=200, Constitution=20/100,
              tier=2)
barhas = Star("Bards_Harp", "Second Bards Harp Star", rank=1, Pierce_Damage=40/100, Elemental_Damage=40/100,
              Increases_Energy_Regeneration=10/100)
barhat = Star("Bards_Harp", "Third Bards Harp Star", rank=2, Pierce_Resistance=15/100, Bleeding_Resistance=10/100)
barhaft = Star("Bards_Harp", "Fourth Bards Harp Star", rank=3, Energy=10/100, Energy_Regenerated_per_Second=2)
barhaff = Star("Bards_Harp", "Fifth Bards Harp Star", rank=4, Pierce_Damage=50/100, Elemental_Damage=50/100,
               Elemental_Resistance=15/100)
inspiration = Star("Bards_Harp", "Inspiration", rank=5, Seconds_Skill_Recharge=12, Seconds_Duration=6,
                   Meter_Radius=15, Energy_Restored=25/100, Offensive_Ability=110, Defensive_Ability=110,
                   Energy_Regenerated_per_Second=7, Slow_Resistance=45/100, Reduced_Entrapment_Duration=45/100)
bards_harp = Constellation("Bards_Harp", {Points_of_Primordial.name: 2, Points_of_Order.name: 2},
                           {Points_of_Primordial.name: 6, str(Points_of_Ascendant.name): 6, Points_of_Order.name: 3},
                           [barhaf, barhas, barhat, barhaft, barhaft, barhaff, inspiration], tier=2)

azraaf = Star("Azraaka_the_Eternal_Sands", "First Azraaka the Eternal Sands Star", [12, 8, 6],
              [Points_of_Ascendant, Points_of_Primordial, Points_of_Order], [0],
              [Points_of_Ascendant, Points_of_Primordial, Points_of_Order], rank=0, Physical_Damage=80/100,
              Pierce_Damage=80/100, tier=3)
azraas = Star("Azraaka_the_Eternal_Sands", "Second Azraaka the Eternal Sands Star", rank=1, Health=180, Armor=90)
azraat = Star("Azraaka_the_Eternal_Sands", "Third Azraaka the Eternal Sands Star", rank=2, Health=180,
              Defensive_Ability=50, Movement_Speed=6/100)
azraaft = Star("Azraaka_the_Eternal_Sands", "Fourth Azraaka the Eternal Sands Star", line=1, rank=3,
               Defensive_Ability=50, Attack_Speed=6/100, Casting_Speed=6/100)
azraaff = Star("Azraaka_the_Eternal_Sands", "Fifth Azraaka the Eternal Sands Star", line=2, rank=3,
               Pierce_Damage=[range(9, 11), 100/100], Physical_Damage=100/100)
shifting_sands = Star("Azraaka_the_Eternal_Sands", "Shifting Sands", line=2, rank=4, Seconds_Skill_Recharge=0.5,
                      Seconds_Duration=1, Chance_to_pass_through_Enemies=100/100, Meter_Radius=2, Weapon_Damage=30/100,
                      Physical_Damage=205, Pierce_Damage=301, Crit_Damage=40/100, Reduced_target_Offensive_Ability=140,
                      Chance_of_Impaired_Aim_to_Target=25/100)
azraaka_the_eternal_sands = Constellation('Azraaka_the_Eternal_Sands', [],
                                          {Points_of_Ascendant.name: 12, Points_of_Primordial.name: 8,
                                           Points_of_Order.name: 6},
                                          [azraaf, azraas, azraat, azraaft, azraaff, shifting_sands], tier=3)

shief = Star("Shieldmaiden", "First Shieldmaiden Star", [6, 4], [Points_of_Primordial, Points_of_Order], [3, 2],
             [Points_of_Primordial, Points_of_Order], rank=0, Shield_Damage_Blocked=15/100, tier=2)
shies = Star("Shieldmaiden", "Second Shieldmaiden Star", rank=1, Internal_Trauma_Damage=50/100,
             to_All_Retaliation_Damage=50/100)
shiet = Star("Shieldmaiden", "Third Shieldmaiden Star", line=1, rank=2, Shield_Block_Chance=6/100)
shieft = Star("Shieldmaiden", "Fourth Shieldmaiden Star", line=1, rank=3,  Internal_Trauma_Damage=60,
              Physical_Damage_Retaliation=200)
shieff = Star("Shieldmaiden", "Fifth Shieldmaiden Star", line=2, rank=2, Reduced_Stun_Duration=25/100,
              Shield_Damage_Blocked=20/100)
shiest = Star("Shieldmaiden", "Sixth Shieldmaiden Star", line=2, rank=3, Shield_Recovery=25/100,
              Shield_Damage_Blocked=10/100)
shieldmaiden = Constellation("Shieldmaiden", {Points_of_Primordial.name: 3, Points_of_Order.name: 2},
                             {Points_of_Primordial.name: 6, str(Points_of_Order.name): 4},
                             [shief, shies, shiet, shieft, shieff, shiest], tier=2)

ulof = Star("Ulo_the_Keeper_of_The_Waters", "First Ulo the Keeper of The Waters Star", [6, 4],
            [Points_of_Primordial, Points_of_Order], [3, 2], [Points_of_Primordial, Points_of_Order], rank=0,
            Elemental_Resistance=10/100, pets_Elemental_Resistance=10/100, tier=2)
ulos = Star("Ulo_the_Keeper_of_The_Waters", "Second Ulo the Keeper of The Waters Star", rank=1, Health=200, Energy=200,
            Life_Leech_Resistance=30/100, Energy_Leech_Resistance=30/100)
ulot = Star("Ulo_the_Keeper_of_The_Waters", "Third Ulo the Keeper of The Waters Star", line=1, rank=2,
            Reduced_Stun_Duration=10/100, Reduced_Petrify_Duration=10/100, Reduced_Freeze_Duration=10/100)
uloft = Star("Ulo_the_Keeper_of_The_Waters", "Fourth Ulo the Keeper of The Waters Star", line=2, rank=2,
             Poison_and_Acid_Resistance=15/100, Chaos_Resistance=10/100, pets_Poison_and_Acid_Resistance=15/100,
             pets_Chaos_Resistance=10/100)
cleansing_waters = Star("Ulo_the_Keeper_of_The_Waters", "Cleansing Waters", line=3, rank=2, Seconds_Skill_Recharge=16,
                        Second_Duration=1, Meter_Radius=3, Slow_Target=[50/100, 8])
ulo_the_keeper_of_the_waters = Constellation("Ulo_the_Keeper_of_The_Waters",
                                             {Points_of_Primordial.name: 3, Points_of_Order.name: 2},
                                             {Points_of_Primordial.name: 6, Points_of_Order.name: 4},
                                             [ulof, ulos, ulot, uloft, cleansing_waters], tier=2)

menhif = Star("Obelisk_of_Menhir", "First Obelisk of Menhir Star", [15, 8], [Points_of_Primordial, Points_of_Order],
              [0], [Points_of_Primordial, Points_of_Order], rank=0, Armor=10/100, tier=3)
menhis = Star("Obelisk_of_Menhir", "Second Obelisk of Menhir Star", line=1, rank=1, Physical_Damage_Retaliation=120,
              to_All_Retaliation_Damage=60/100)
menhit = Star("Obelisk_of_Menhir", "Third Obelisk of Menhir Star", line=1, rank=2, Shield_Block_Chance=5/100,
              Shield_Damage_Blocked=30/100)
menhift = Star("Obelisk_of_Menhir", "Fourth Obelisk of Menhir Star", line=1, rank=3, Reduced_Stun_Duration=30/100,
               Reduced_Freeze_Duration=30/100, Increases_Armor_Absorption=18/100, Maximum_Pierce_Resistance=3/100)
menhiff = Star("Obelisk_of_Menhir", "Fifth Obelisk of Menhir Star", line=2, rank=1, Defensive_Ability=30, Armor=150)
menhist = Star("Obelisk_of_Menhir", "Sixth Obelisk of Menhir Star", line=2, rank=2, Defensive_Ability=[25, 25/100])
stone_form = Star("Obelisk_of_Menhir", "Stone Form", line=1, rank=4, Seconds_Skill_Recharge=12, Seconds_Duration=8,
                  Meter_Radius=15, Damage_Absorption=400, Reduction_in_Bleeding_Duration=50/100,
                  Reduction_in_Poison_Duration=50/100, to_All_Retaliation_Damage=115/100)
obelisk_of_menhir = Constellation('Obelisk_of_Menhir', [], {Points_of_Primordial.name: 15, Points_of_Order.name: 8},
                                  [menhif, menhis, menhit, menhift, menhiff, menhist, stone_form], tier=3)

empyriof = Star("Light_of_Empyrion", "First Light of Empyrion Star", [18, 8], [Points_of_Primordial, Points_of_Order],
                [0], [Points_of_Primordial, Points_of_Order], rank=0, Elemental_Resistance=15/100,
                pets_Elemental_Resistance=15/100, tier=3)
empyrios = Star("Light_of_Empyrion", "Second Light of Empyrion Star", rank=1, Physical_Damage=80/100,
                Fire_Damage=80/100, Damage_to_Chthonics=10/100, Defensive_Ability=30)
empyriot = Star("Light_of_Empyrion", "Third Light of Empyrion Star", rank=2, Health=6/100, pets_Health=6/100)
empyrioft = Star("Light_of_Empyrion", "Fourth Light of Empyrion Star", rank=3, Health=4/100, Vitality_Resistance=15/100,
                 pets_Health=4/100, pets_Vitality_Resistance=15/100)
empyrioff = Star("Light_of_Empyrion", "Fifth Light of Empyrion Star", rank=4, Aether_Resistance=20/100,
                 Chaos_Resistance=20/100, pets_Aether_Resistance=20/100, pets_Chaos_Resistance=20/100)
empyriost = Star("Light_of_Empyrion", "Sixth Light of Empyrion Star", rank=5, Physical_Damage=range(6, 8),
                 Fire_Damage=range(6, 10), Maximum_Aether_Resistance=3/100, Maximum_Chaos_Resistance=3/100,
                 pets_all_res=5/100)
empyrions_light = Star("Light_of_Empyrion", "Light of Empyrion", rank=6, Seconds_Skill_Recharge=2.5,
                       Meter_Target_Area=5, Weapon_Damage=54/100, Physical_Damage=315, Fire_Damage=range(280, 385),
                       Knockdown=1.5, Reduced_target_Damage=24/100, Damage_to_Undead=50/100, Damage_to_Chthonics=50/100,
                       pets_Maximum_all_Resistances=5/100)
light_of_empyrion = Constellation("Light_of_Empyrion", [], {Points_of_Primordial.name: 18, Points_of_Order.name: 8},
                                  [empyriof, empyrios, empyriot, empyrioft, empyrioff, empyriost, empyrions_light],
                                  tier=3)

ishtaf = Star("Ishtak_the_Spring_Maiden", "First Ishtak the Spring Maiden Star", [15, 10],
              [Points_of_Primordial, Points_of_Order], [0], [Points_of_Primordial, Points_of_Order], rank=0, Health=300,
              Energy=300, pets_Physical_Damage=8, tier=3)
ishtas = Star("Ishtak_the_Spring_Maiden", "Second Ishtak the Spring Maiden Star", rank=1, Spirit=3/100,
              Defensive_Ability=3/100, pets_Defensive_Ability=3/100, pets_Resistance_to_Life_Reduction=20/100)
ishtat = Star("Ishtak_the_Spring_Maiden", "Third Ishtak the Spring Maiden Star", rank=2, Total_Speed=4/100,
              Slow_Resistance=30/100, pets_Total_Speed=6/100)
ishtaft = Star("Ishtak_the_Spring_Maiden", "Fourth Ishtak the Spring Maiden Star", rank=3, Health=300,
               Bleeding_Resistance=20/100, pets_Bleeding_Resistance=20/100)
ishtaff = Star("Ishtak_the_Spring_Maiden", "Fifth Ishtak the Spring Maiden Star", rank=4, Health=300,
               Poison_and_Acid_Resistance=25/100, pets_Poison_and_Acid_Resistance=25/100)
natures_guardians = Star("Ishtak_the_Spring_Maiden", "Natures Guardians", rank=5, Seconds_Skill_Recharge=15,
                         Seconds_Duration=6, Damage_Absorption=25/100, pets_Physical_Damage=40,
                         pets_Offensive_Ability=130, pets_Defensive_Ability=130, pets_Taunt_Target=True)
ishtak_the_spring_maiden = Constellation("Ishtak_the_Spring_Maiden", [],
                                         {Points_of_Primordial.name: 15, Points_of_Order.name: 10},
                                         [ishtaf, ishtas, ishtat, ishtaft, ishtaff, natures_guardians], tier=2)

treef = Star("Tree_of_Life", "First Tree of Life Star", [20, 7], [Points_of_Primordial, Points_of_Order], [0],
             [Points_of_Primordial, Points_of_Order], rank=0, Health=5/100, pets_Health=5/100, tier=3)
trees = Star("Tree_of_Life", "Second Tree of Life Star", rank=1, Health_Regenerated_Per_Second=30,
             pets_Increases_Health_Regeneration=50/100)
treet = Star("Tree_of_Life", "Third Tree of Life Star", line=1, rank=2, Health=8/100,
             Increases_Health_Regeneration=50/100, pets_Health=5/100)
treeff = Star("Tree_of_Life", "Fifth Tree of Life Star", rank=3, line=2, pets_Health_Regenerated_Per_Second=80,
              Increases_Health_Regeneration=50/100, Health=8/100)
treeft = Star("Tree_of_Life", "Fourth Tree of Life Star", rank=2, pets_Increases_Health_Regeneration=50/100,
              Defensive_Ability=30, Health_Regenerated_Per_Second=50)
healing_rain = Star("Tree_of_Life", "Healing Rain", rank=3, line=3, Seconds_Skill_Recharge=12, Seconds_Duration=8,
                    Meter_Radius=15, Health_Restored=[10/100, 700], Health_Regenerated_Per_Second=180,
                    Increases_Health_Regeneration=60/100, Energy_Regenerated_per_Second=12,
                    Increases_Energy_Regeneration=55/100)
tree_of_life = Constellation("Tree_of_Life", [], {Points_of_Order.name: 7, Points_of_Primordial.name: 20},
                             [treef, trees, treet, treeft, treeff, healing_rain], tier=3)

korvaf = Star("Korvak_The_Eldritch_Sun", "First Korvak The Eldritch Sun Star", [18, 10],
              [Points_of_Primordial, Points_of_Eldritch], [0], [Points_of_Primordial, Points_of_Eldritch],
              rank=0, to_All_Damage=30/100, pets_to_All_Damage=30/100, tier=3)
korvas = Star("Korvak_The_Eldritch_Sun", "Second Korvak The Eldritch Sun Star", rank=1, Health=6/100, pets_Health=6/100)
korvat = Star("Korvak_The_Eldritch_Sun", "Third Korvak The Eldritch Sun Star", rank=2, Chaos_Resistance=20/100,
              pets_Chaos_Resistance=20/100)
korvaft = Star("Korvak_The_Eldritch_Sun", "Fourth Korvak The Eldritch Sun Star", rank=3, line=1, to_All_Damage=50/100,
               Crit_Damage=8/100, pets_to_All_Damage=30/100, pets_Crit_Damage=8/100)
korvaff = Star("Korvak_The_Eldritch_Sun", "Fifth Korvak The Eldritch Sun Star", line=2, rank=3, to_All_Damage=50/100,
               pets_to_All_Damage=30/100, pets_Offensive_Ability=5/100, Offensive_Ability=5/100)
korvak_eye = Star("Korvak_The_Eldritch_Sun", "Eye Of Korvak", line=3, rank=3, Seconds_Skill_Recharge=1.5, Projectiles=6,
                  Meter_Radius=1, Chance_to_pass_through_Enemies=100/100, Weapon_Damage=18/100,
                  Chance_to_Petrify_Target=[50/100, 1.5], Reduced_target_Offensive_Ability=130,
                  Reduced_target_Defensive_Ability=130)
korvak_the_eldritch_sun = Constellation("Korvak_The_Eldritch_Sun", [],
                                        {Points_of_Primordial.name: 18, Points_of_Eldritch.name: 10},
                                        [korvaf, korvas, korvat, korvaft, korvaff, korvak_eye], tier=3)

viref = Star("Vire_the_Stone_Matron", "First Vire the Stone Matron Star", [18, 12],
             [Points_of_Primordial, Points_of_Ascendant], [0], [Points_of_Primordial, Points_of_Ascendant],
             rank=0, Health=200, Armor=75, tier=3)
vires = Star("Vire_the_Stone_Matron", "Second Vire the Stone Matron Star", rank=1, Aether_Resistance=10/100,
             Chaos_Resistance=10/100, Physical_Damage_Retaliation=100)
viret = Star("Vire_the_Stone_Matron", "Third Vire the Stone Matron Star", rank=2, Health=8/100, Armor=40,
             Shield_Damage_Blocked=12/100)
vireft = Star("Vire_the_Stone_Matron", "Fourth Vire the Stone Matron Star", line=1, rank=3, Physical_Damage=80/100,
              Internal_Trauma_Damage=80/100, Cunning=3/100, to_All_Retaliation_Damage=100/100)
vireff = Star("Vire_the_Stone_Matron", "Fifth Vire the Stone Matron Star", line=2, rank=3, Physical_Resistance=4/100,
              Pierce_Resistance=20/100, Bleeding_Resistance=20/100)
vire_fist = Star("Vire_the_Stone_Matron", "Fist of Vire", line=2, rank=4, Seconds_Skill_Recharge=1, Second_Duration=1,
                 Meter_Radius=2.5, Weapon_Damage=65/100, of_Retaliation_Damage_added_to_Attack=20/100,
                 Physical_Damage=245, Internal_Trauma_Damage=1220, Reduced_target_Physical_Damage=20/100,
                 Chance_to_Petrify_Target=2)
vire_the_stone_matron = Constellation('Vire_the_Stone_Matron', [],
                                      {Points_of_Primordial.name: 18, Points_of_Ascendant.name: 12},
                                      [viref, vires, viret, vireft, vireff, vire_fist], tier=3)

aeof = Star("Aeons_Hourglass", "First Aeons Hourglass Star", [18, 8], [Points_of_Primordial, Points_of_Chaos], [0],
            [Points_of_Primordial, Points_of_Chaos], rank=0, Physique=40, Cunning=40, Spirit=40, tier=3)
aeos = Star("Aeons_Hourglass", "Second Aeons Hourglass Star", rank=1,
            Reduction_in_Internal_Trauma_Seconds_Duration=25/100, Reduction_in_Bleeding_Seconds_Duration=25/100,
            Reduction_in_Poison_Seconds_Duration=25/100, Reduction_in_Burn_Seconds_Duration=25/100,
            Reduction_in_Frostbite_Seconds_Duration=25/100, Reduction_in_Electrocute_Seconds_Duration=25/100,
            Reduction_in_Vitality_Decay_Seconds_Duration=25/100)
aeot = Star("Aeons_Hourglass", "Third Aeons Hourglass Star", rank=2, Slow_Resistance=50/100,
            Reduced_Entrapment_Duration=30/100, Reflected_Damage_Reduction=25/100)
aeoft = Star("Aeons_Hourglass", "Fourth Aeons Hourglass Star", rank=3, Vitality_Resistance=15/100,
             Aether_Resistance=20/100, Maximum_Vitality_Resistance=4/100)
aeoff = Star("Aeons_Hourglass", "Fifth Aeons Hourglass Star", rank=4, Defensive_Ability=45,
             Chance_to_Avoid_Melee_Attacks=6/100, Chance_to_Avoid_Projectiles=6/100)
time_dilation = Star("Aeons_Hourglass", "Time Dilation", rank=5, Seconds_to_All_Currently_Active_Skills_Cooldowns=-6,
                     Seconds_Skill_Recharge=16)
aeons_hourglass = Constellation("Aeons_Hourglass", [], {Points_of_Primordial.name: 18, Points_of_Chaos.name: 8},
                                [aeof, aeos, aeot, aeoft, aeoff, time_dilation], tier=3)

revef = Star("Revenant", "First Revenant Star", [8], [Points_of_Primordial, Points_of_Chaos], [1, 1], [Points_of_Chaos],
             rank=0, Energy_Leech_Chance=40, Energy_Absorbed_From_Enemy_Spells=15/100, tier=2)
reves = Star("Revenant", "Second Revenant Star", rank=1, Less_Damage_from_Undead=10/100, Health=3/100)
revet = Star("Revenant", "Third Revenant Star", rank=2, Vitality_Resistance=24/100, pets_Vitality_Resistance=15/100)
reveft = Star("Revenant", "Fourth Revenant Star", rank=3, Health=175, of_Attack_Damage_Converted_To_Health=6/100)
reveff = Star("Revenant", "Fifth Revenant Star", rank=4, Attack_Speed=4/100, Casting_Speed=4/100)
raise_dead = Star("Revenant", "Raise the Dead", rank=5, Seconds_Skill_Recharge=2, Summon_Limit=6,
                  Skeleton_Attributes={'attr1': 'Lives for 20 Seconds attr', 'attr2': 'Invincible attr',
                                       'attr3': '1793 Energy attr'},
                  Melee_Attack={'skl1': '140 Vitality Damage skl', 'skl2': '118 Aether Damage skl',
                                'skl3': '45% Slower Target Movement for 3 Seconds skl',
                                'skl4': "24 Reduced target's Resistances skl"})
revenant = Constellation("Revenant", {Points_of_Primordial.name: 1, Points_of_Chaos.name: 1},
                         {Points_of_Chaos.name: 8}, [revef, reves, revet, reveft, reveff, raise_dead], tier=2)

dygof = Star("Dying_God", "First Dying God Star", [15, 8], [Points_of_Primordial, Points_of_Chaos], [0],
             [Points_of_Primordial, Points_of_Chaos], rank=0, Vitality_Damage=80/100, Offensive_Ability=20, tier=3)
dygos = Star("Dying_God", "Second Dying God Star", rank=1, Chaos_Damage=80/100, Offensive_Ability=20)
dygot = Star("Dying_God", "Third Dying God Star", rank=2, Spirit=35, Offensive_Ability=3/100,
             pets_to_All_Damage=30/100, pets_Attack_Speed=5/100)
dygoft = Star("Dying_God", "Fourth Dying God Star", rank=3, Offensive_Ability=45, Defensive_Ability=25,
              Chaos_Resistance=15/100)
dygoff = Star("Dying_God", "Fifth Dying God Star", rank=4, Vitality_Damage=100/100, Chaos_Damage=100/100)
dygost = Star("Dying_God", "Sixth Dying God Star", line=1, rank=5, Chaos_Damage=range(5, 18), Crit_Damage=4/100,
              pets_to_All_Damage=60/100, pets_Crit_Damage=10/100, )
hungering_void = Star("Dying_God", "Hungering Void", line=2, rank=5, Health_cost=308, Seconds_Skill_Recharge=30,
                      Seconds_Duration=20, Meter_Radius=12, Crit_Damage=18/100, Vitality_Damage=370/100,
                      Chaos_Damage=370/100, Vitality_Decay_Damage=370/100, Total_Speed=10/100,
                      Chaos_Retaliation_Damage=720, Terrify_Chance=70/100, pets_to_All_Damage=200/100,
                      pets_Crit_Damage=20/100, pets_Chance_to_Stun_Target=[10/100, 1],
                      pets_Chance_of_Slow_Target=[56/100, 0.3, 3])
dying_god = Constellation("Dying_God", [], {Points_of_Primordial.name: 15, Points_of_Chaos.name: 8},
                          [dygof, dygos, dygot, dygoft, dygoff, dygost, hungering_void], tier=3)

yugof = Star("Yugol_The_Insatiable_Night", "First Yugol The Insatiable Night Star", [20, 7],
             [Points_of_Eldritch, Points_of_Chaos], [0], [Points_of_Eldritch, Points_of_Chaos], rank=0,
             Cold_Damage=80/100, Offensive_Ability=25, tier=3)
yugos = Star("Yugol_The_Insatiable_Night", "Second Yugol The Insatiable Night Star", rank=1, Acid_Damage=80/100,
             Offensive_Ability=25)
yugot = Star("Yugol_The_Insatiable_Night", "Third Yugol The Insatiable Night Star", rank=2, Vitality_Resistance=25/100,
             Reflected_Damage_Reduction=10/100, )
yugoft = Star("Yugol_The_Insatiable_Night", "Fourth Yugol The Insatiable Night Star", line=1, rank=3,
              Cold_Damage=100/100, Acid_Damage=100/100, Spirit=3/100)
yugoff = Star("Yugol_The_Insatiable_Night", "Fifth Yugol The Insatiable Night Star", line=2, rank=3, Cold_Damage=5,
              Acid_Damage=5, of_Attack_Damage_Converted_To_Health=6/100, Life_Leech_Resistance=40/100)
yougol_blood = Star("Yugol_The_Insatiable_Night", "Black Blood of Yugol", line=2, rank=4, Seconds_Skill_Recharge=0.8,
                    Summon_Limit=6, Meter_Radius=3,
                    Black_Blood_of_Yugol_Attributes={'attr1': 'Invincible attr', 'attr2': 'Lives for 6 Seconds attr',
                                                     'attr3': '300 Energy attr'},
                    Black_Blood={'skl1': '330 Acid Damage skl', 'skl2': '330 Cold Damage skl',
                                 'skl3': '16% Reduced target Damage skl', 'skl4': '-30% Movement Speed skl',
                                 'skl5': '-100% Increase Health Regeneration skl'})
yugol_the_insatiable_night = Constellation("Yugol_The_Insatiable_Night", [],
                                           {Points_of_Eldritch.name: 20, Points_of_Chaos.name: 7},
                                           [yugof, yugos, yugot, yugoft, yugoff, yougol_blood], tier=3)

wendif = Star("Wendigo", "First Wendigo Star", [6, 4], [Points_of_Chaos], [2], [Points_of_Primordial, Points_of_Chaos],
              rank=0, Vitality_Damage=40/100, Vitality_Decay=40/100, tier=2)
wendis = Star("Wendigo", "Second Wendigo Star", rank=1, Spirit=20, Health=150)
wendit = Star("Wendigo", "Third Wendigo Star", rank=2, Casting_Speed=5/100, Physical_Resistance=4/100,
              Attack_Speed=5/100)
wendift = Star("Wendigo", "Fourth Wendigo Star", rank=3, Less_Damage_From_Beasts=10/100, Health=5/100)
wendiff = Star("Wendigo", "Fifth Wendigo Star", rank=4, Vitality_Decay=[36, 50/100], Vitality_Damage=50/100)
wendigos_mark = Star("Wendigo", "Wendigos Mark", rank=5, Seconds_Duration=10, Vitality_Damage=210,
                     of_Attack_Damage_Converted_To_Health=65/100)
wendigo = Constellation("Wendigo", {Points_of_Chaos.name: 2}, {Points_of_Primordial.name: 6,
                                                               Points_of_Chaos.name: 4},
                        [wendif, wendis, wendit, wendift, wendiff, wendigos_mark], tier=2)

hydraf = Star("Hydra", "First Hydra Star", [5, 3, 3], [Points_of_Eldritch, Points_of_Chaos], [3, 2],
              [Points_of_Eldritch, Points_of_Ascendant, Points_of_Chaos], rank=0, Offensive_Ability=25, tier=2)
hydras = Star("Hydra", "Second Hydra Star", rank=1, Offensive_Ability=35)
hydrat = Star("Hydra", "Third Hydra Star", line=3, rank=2, Attack_Speed=5/100, to_All_Damage=50/100)
hydraft = Star("Hydra", "Fourth Hydra Star", line=2, rank=2, of_Attack_Damage_Converted_To_Health=4/100,
               Attack_Speed=5/100)
hydraff = Star("Hydra", "Fifth Hydra Star", line=1, rank=2, Offensive_Ability=25,  Physical_Damage=6)
hydrast = Star("Hydra", "Sixth Hydra Star", line=1, rank=3, Offensive_Ability=4/100, Slow_Resistance=20/100,
               Physical_Damage=12)
hydra = Constellation("Hydra", {Points_of_Eldritch.name: 3, Points_of_Chaos.name: 2},
                      {Points_of_Eldritch.name: 5, Points_of_Ascendant.name: 3, Points_of_Chaos.name: 3},
                      [hydraf, hydras, hydrat, hydraft, hydraft, hydraff, hydrast], tier=2)

ulzuf = Star("Ulzuins_Torch", "First Ulzuins Torch Star", [15, 8], [Points_of_Eldritch, Points_of_Chaos], [0],
             [Points_of_Eldritch, Points_of_Chaos], rank=0, Offensive_Ability=20, Fire_Damage=80/100, tier=3)
ulzus = Star("Ulzuins_Torch", "Second Ulzuins Torch Star", rank=1, Chaos_Resistance=15/100, Offensive_Ability=5/100)
ulzut = Star("Ulzuins_Torch", "Third Ulzuins Torch Star", rank=2, Movement_Speed=5/100, Crit_Damage=5/100)
ulzuft = Star("Ulzuins_Torch", "Fourth Ulzuins Torch Star", line=1, rank=3,  Burn_Damage=100/100)
ulzuff = Star("Ulzuins_Torch", "Fifth Ulzuins Torch Star", line=2, rank=3, Fire_Resistance=20/100, Fire_Damage=100/100)
ulzust = Star("Ulzuins_Torch", "Sixth Ulzuins Torch Star", line=2, rank=4, Burn_Damage=[54, 100/100],
              Maximum_Fire_Resistance=3/100)
meteor_shower = Star("Ulzuins_Torch", "Meteor Shower", line=1, rank=4, Seconds_Skill_Recharge=3.5, Seconds_Duration=3,
                     Projectiles=1, Meter_Target_Area=5, Meter_Radius=2.4, Physical_Damage=range(185, 210),
                     Fire_Damage=range(190, 232), Burn_Damage=410)
ulzuins_torch = Constellation("Ulzuins_Torch", [], {str(Points_of_Eldritch.name): 15, str(Points_of_Chaos.name): 8},
                              [ulzuf, ulzus, ulzut, ulzuft, ulzuff, ulzust, meteor_shower], tier=3)

hyriaf = Star("Hyrian_Guardian_of_the_Celestial_Gates", "First Hyrian Guardian of the Celestial Gates Star", [8, 6],
              [Points_of_Ascendant, Points_of_Primordial], [2, 2], [Points_of_Eldritch, Points_of_Ascendant], rank=0,
              Elemental_Damage=40/100, to_All_Retaliation_Damage=40/100, tier=2)
hyrias = Star("Hyrian_Guardian_of_the_Celestial_Gates", "Second Hyrian Guardian of the Celestial Gates Star", rank=1,
              Pierce_Resistance=10/100, Shield_Damage_Blocked=20/100)
hyriat = Star("Hyrian_Guardian_of_the_Celestial_Gates", "Third Hyrian Guardian of the Celestial Gates Star", rank=2,
              Health=200, Healing_Effects_Increased=10/100, Armor=8/100)
hyriaft = Star("Hyrian_Guardian_of_the_Celestial_Gates", "Fourth Hyrian Guardian of the Celestial Gates Star", line=1,
               rank=3, Elemental_Damage=12, Shield_Damage_Blocked=35/100, to_All_Retaliation_Damage=60/100)
hyriaff = Star("Hyrian_Guardian_of_the_Celestial_Gates", "Fifth Hyrian Guardian of the Celestial Gates Star", line=2,
               rank=3, Elemental_Resistance=15/100, Elemental_Damage=50/100, Armor=8/100)
hyrians_glare = Star("Hyrian_Guardian_of_the_Celestial_Gates", "Hyrians Glare", line=2, rank=4,
                     Seconds_Skill_Recharge=2, Meter_Range=10, Weapon_Damage=70/100,
                     of_Retaliation_Damage_added_to_Attack=26/100, Elemental_Damage=280, Chance_to_Confuse=[100/100, 1])
hyrian_guardian_of_the_celestial_gates = Constellation("Hyrian_Guardian_of_the_Celestial_Gates",
                                                       {Points_of_Primordial.name: 2, Points_of_Ascendant.name: 2},
                                                       {Points_of_Eldritch.name: 8, str(Points_of_Ascendant.name): 6},
                                                       [hyriaf, hyrias, hyriat, hyriaft, hyriaff, hyrians_glare],
                                                       tier=2)

magif = Star("Magi", "First Magi Star", [10], [Points_of_Eldritch], [3], [Points_of_Eldritch], rank=0,
             Fire_Damage=40/100, Burn_Damage=50/100, tier=2)
magis = Star("Magi", "Second Magi Star", rank=1, Elemental_Resistance=8/100, Defensive_Ability=10)
magit = Star("Magi", "Third Magi Star", rank=2, Defensive_Ability=10, Fire_Resistance=25/100,
             Reduced_Entrapment_Duration=15/100)
magift = Star("Magi", "Fourth Magi Star", line=1, rank=3, Fire_Damage=[range(9, 12), 40/100])
magiff = Star("Magi", "Fifth Magi Star", line=2, rank=3, Casting_Speed=5/100, Physique=15, Burn_Damage=100/100,
              Attack_Speed=5/100)
magist = Star("Magi", "Sixth Magi Star", line=3, rank=3.1, Burn_Damage=[36, 50/100])
fissure = Star("Magi", "Fissure", line=3, rank=4, Seconds_Skill_Recharge=1.5, Seconds_Duration=5, Fragments=range(6, 8),
               Meter_Radius=1, Fire_Damage=range(160, 198), Burn_Damage=328, Chance_to_Stun=[25/100, 1.5])
magi = Constellation("Magi", {Points_of_Eldritch.name: 3}, {str(Points_of_Eldritch.name): 10},
                     [magif, magis, magit, magift, magiff, magist, fissure], tier=2)

lantef = Star("Oklaines_Lantern", "First Oklaines Lantern Star", [10], [Points_of_Eldritch, Points_of_Order], [3, 2],
              [Points_of_Eldritch], rank=0, Increases_Energy_Regeneration=15/100, tier=2)
lantes = Star("Oklaines_Lantern", "Second Oklaines Lantern Star", rank=1, Offensive_Ability=25, Defensive_Ability=20)
lantet = Star("Oklaines_Lantern", "Third Oklaines Lantern Star", rank=2, Crit_Damage=5/100, Offensive_Ability=15)
lanteft = Star("Oklaines_Lantern", "Fourth Oklaines Lantern Star", rank=3, to_All_Damage=50/100,
               Reduced_Entrapment_Duration=25/100)
lanteff = Star("Oklaines_Lantern", "Fifth Oklaines Lantern Star", rank=4, Energy_Regenerated_per_Second=2,
               Casting_Speed=5/100, Attack_Speed=5/100)
oklaines_lantern = Constellation("Oklaines_Lantern", {Points_of_Eldritch.name: 3, Points_of_Order.name: 2},
                                 {Points_of_Eldritch.name: 10}, [lantef, lantes, lantet, lanteft, lanteff], tier=2)

behef = Star("Behemoth", "First Behemoth Star", [4, 4, 3], [Points_of_Eldritch, Points_of_Chaos], [3, 2],
             [Points_of_Primordial, Points_of_Eldritch, Points_of_Chaos], rank=0, Health_Regenerated_Per_Second=15,
             tier=2)
behes = Star("Behemoth", "Second Behemoth Star", rank=1, Health=300, pets_Health=5/100)
behet = Star("Behemoth", "Third Behemoth Star", line=1, rank=2, Health_Regenerated_Per_Second=30,
             Healing_Effects_Increased=6/100)
beheft = Star("Behemoth", "Fourth Behemoth Star", line=2, rank=2, Armor=80, Health=5/100)
beheff = Star("Behemoth", "Fifth Behemoth Star", line=3, rank=2, Increases_Health_Regeneration=50/100,
              pets_Increases_Health_Regeneration=100/100)
giants_blood = Star("Behemoth", "Giants blood", line=4, rank=2, Seconds_Skill_Recharge=25, Seconds_Duration=10,
                    Health_Restored=[20/100, 1200], Health_Regenerated_Per_Second=440)
behemoth = Constellation('Behemoth', {Points_of_Eldritch.name: 3, Points_of_Chaos.name: 2},
                         {Points_of_Primordial.name: 4, Points_of_Eldritch.name: 4, Points_of_Chaos.name: 3},
                         [behef, behes, behet, beheft, beheff, giants_blood], tier=2)

abomif = Star("Abomination", "First Abomination Star", [18, 8], [Points_of_Eldritch, Points_of_Chaos], [0],
              [Points_of_Eldritch, Points_of_Chaos], line=None, rank=0, Chaos_Damage=80/100, Poison_Damage=80/100,
              tier=3)
abomis = Star("Abomination", "Second Abomination Star", rank=1, Acid_Damage=80/100, Vitality_Damage=80/100,
              Vitality_Decay=80/100)
abomit = Star("Abomination", "Third Abomination Star", rank=2, Offensive_Ability=40, Poison_and_Acid_Resistance=20/100,
              Maximum_Poison_and_Acid_Resistance=3/100)
abomift = Star("Abomination", "Fourth Abomination Star", line=1, rank=3, Chaos_Damage=80/100, Health=250,
               Offensive_Ability=30, Vitality_Damage=80/100)
abomiff = Star("Abomination", "Fifth Abomination Star", line=2, rank=3, Poison_Damage=80/100, Health=250,
               Offensive_Ability=30, Vitality_Decay=80/100)
abomist = Star("Abomination", "Sixth Abomination Star", line=2, rank=4, Acid_Damage=[12, 100/100],
               Poison_Damage=100/100)
abominable_might = Star("Abomination", "Abominable Might", line=1, rank=4, Seconds_Skill_Recharge=18,
                        Seconds_Duration=12, Chaos_Damage=[range(54, 135), 260/100],
                        Physical_Damage_Converted_to_Chaos_Damage=50/100, Increases_Health_Regeneration=100/100,
                        Vitality_Damage=310/100, Vitality_Decay=310/100)
tainted_eruption = Star("Abomination", "Tainted Eruption", line=2, rank=5, Seconds_Skill_Recharge=3,
                        Meter_Target_Area=10, Poison_Damage=1560, Chance_to_Confuse=1.8)
abomination = Constellation("Abomination", [], {str(Points_of_Eldritch.name): 18, Points_of_Chaos.name: 8},
                            [abomif, abomis, abomit, abomift, abomiff, abomist, abominable_might, tainted_eruption],
                            tier=3)

murmuf = Star("Murmur_Mistress_of_Rumors", "First Murmur Mistress of Rumors Star", [6, 6, 3],
              [Points_of_Eldritch, Points_of_Chaos], [2, 2],
              [Points_of_Eldritch, Points_of_Primordial, Points_of_Chaos], rank=0, Cold_Damage=40/100,
              Acid_Damage=40/100, tier=2)
murmus = Star("Murmur_Mistress_of_Rumors", "Second Murmur Mistress of Rumors Star", rank=1,
              Chance_to_Avoid_Melee_Attacks=3/100, Chance_to_Avoid_Projectiles=3/100)
murmut = Star("Murmur_Mistress_of_Rumors", "Third Murmur Mistress of Rumors Star", rank=2, Defensive_Ability=15,
              Health=150)
murmuft = Star("Murmur_Mistress_of_Rumors", "Fourth Murmur Mistress of Rumors Star", line=2, rank=4,
               Defensive_Ability=15, Vitality_Resistance=10/100)
murmuff = Star("Murmur_Mistress_of_Rumors", "Fifth Murmur Mistress of Rumors Star", line=1, rank=4, Cold_Damage=50/100,
               Acid_Damage=50/100, Frostburn_Damage=80/100)
rumor = Star("Murmur_Mistress_of_Rumors", "Rumor", rank=3, Seconds_Skill_Recharge=1, Seconds_Duration=4, Cold_Damage=97,
             Acid_Damage=97, Offensive_Ability=-96, Cold_Resistance=-23/100, Poison_and_Acid_Resistance=-30/100)
murmur_mistress_of_rumors = Constellation("Murmur_Mistress_of_Rumors",
                                          {Points_of_Eldritch.name: 2, Points_of_Chaos.name: 2},
                                          {Points_of_Eldritch.name: 6, str(Points_of_Primordial.name): 6,
                                           Points_of_Chaos.name: 3}, [murmuf, murmus, murmut, rumor, murmuft, murmuff],
                                          tier=2)

alladraf = Star("Alladrahs_Phoenix", "First Alladrahs Phoenix Star", [6, 6, 3], [Points_of_Eldritch,
                                                                                 Points_of_Ascendant],
                [2, 2], [Points_of_Eldritch, Points_of_Primordial, Points_of_Order], rank=0, Aether_Damage=40/100,
                Elemental_Damage=40/100, tier=2)
alladras = Star("Alladrahs_Phoenix", "Second Alladrahs Phoenix Star", rank=1, Health=225, Chaos_Resistance=12/100,
                Fire_Retaliation=200)
alladrat = Star("Alladrahs_Phoenix", "Third Alladrahs Phoenix Star", rank=2, Aether_Damage=30/100,
                Elemental_Damage=30/100, Increases_Health_Regeneration=20/100)
alladraft = Star("Alladrahs_Phoenix", "Fourth Alladrahs Phoenix Star", rank=3, Crit_Damage=10/100, Fire_Damage=50/100,
                 Burn_Damage=100/100, to_All_Retaliation_Damage=60/100)
phoenix_fire = Star("Alladrahs_Phoenix", "Phoenix Fire", rank=4, Seconds_Skill_Recharge=12, Seconds_Duration=7,
                    Meter_Target_Area=5, Damage_Absorbtion=168, Fire_Damage=92, Aether_Damage=92, Burn_Damage=232,
                    Burn_Retaliation=1395, to_All_Retaliation_Damage=140/100)
alladrahs_phoenix = Constellation("Alladrahs_Phoenix", {Points_of_Eldritch.name: 2, Points_of_Ascendant.name: 2},
                                  {Points_of_Eldritch.name: 6, str(Points_of_Primordial.name): 6,
                                   Points_of_Order.name: 3}, [alladraf, alladras, alladrat, alladraft, phoenix_fire],
                                  tier=2)

ultof = Star("Hand_of_Ultos", "First Ultos Shepherd of Storms", [10, 10, 6],
             [Points_of_Eldritch, Points_of_Primordial, Points_of_Chaos], [0],
             [Points_of_Eldritch, Points_of_Primordial, Points_of_Chaos], rank=0, Cold_Damage=80/100,
             Offensive_Ability=25, tier=3)
ultos = Star("Hand_of_Ultos", "Second Ultos Shepherd of Storms Star", rank=1, Lightining_Damage=80/100,
             Offensive_Ability=25)
ultot = Star("Hand_of_Ultos", "Third Ultos Shepherd of Storms Star", line=1, rank=2, Health=180,
             Chaos_Resistance=15/100)
ultoft = Star("Hand_of_Ultos", "Fourth Ultos Shepherd of Storms Star", line=2, rank=2, Crit_Damage=5/100,
              Frostburn_Damage=120/100, Electrocute_Damage=120/100, Offensive_Ability=20)
ultoff = Star("Hand_of_Ultos", "Fifth Ultos Shepherd of Storms Star", line=2, rank=3,
              Lightining_Damage=[range(3, 20), 100/100], Cold_Damage=100/100)
ultos_hand = Star("Hand_of_Ultos", "Hand of Ultos", line=2, rank=4, Seconds_Skill_Recharge=1.5, Affected_Targets=10,
                  Weapon_Damage=20/100, Lightining_Damage=range(222, 434), Electrocute_Damage=510, Chance_to_Stun=0.4,
                  Reduced_target_Elemental_Resistances=20/100)
hand_of_ultos = Constellation("Hand_of_Ultos", [], {Points_of_Eldritch.name: 10, Points_of_Primordial.name: 10,
                                                    Points_of_Chaos.name: 6}, [ultof, ultos, ultot, ultoft, ultoff,
                                                                               ultos_hand], tier=3)

sagef = Star("Blind_Sage", "First Blind Sage Star", [18, 10], [Points_of_Eldritch, Points_of_Ascendant], [0],
             [Points_of_Eldritch, Points_of_Ascendant], rank=0, Physique=30, Spirit=30, Offensive_Ability=25, tier=3)
sages = Star("Blind_Sage", "Second Blind Sage Star", rank=1, Elemental_Resistance=15/100, Offensive_Ability=25,
             Elemental_Damage=80/100)
saget = Star("Blind_Sage", "Third Blind Sage Star", rank=2, Crit_Damage=12/100, Defensive_Ability=25,
             Skill_Disruption_Protection=30/100)
sageft = Star("Blind_Sage", "Fourth Blind Sage Star", line=1, rank=3, Cold_Damage=100/100, Frostburn_Damage=200/100)
sageff = Star("Blind_Sage", "Fifth Blind Sage Star", line=2, rank=3, Lightining_Damage=100/100,
              Electrocute_Damage=200/100)
sagest = Star("Blind_Sage", "Sixth Blind Sage Star", line=3, rank=3, Fire_Damage=100, Burn_Damage=200/100)
elemental_seeker = Star("Blind_Sage", "Elemental Seeker", line=3, rank=4, Seconds_Skill_Recharge=1.2, Meter_Radius=1,
                        Elemental_Seeker_Attributes={'attr1': 'Lives_for 3 Seconds attr', 'attr2': '7448 Health attr',
                                                     'attr3': '300 Energy attr'},
                        Burning_Presence={'skl1': '400 Elemental_Damage skl', 'skl2': '3.8 Meter_Target_Area skl'},
                        Detonate={'skl1': '3.8 Meter_Target_Area acv', 'skl2': '555 Elemental_Damage acv',
                                  'skl3': '62% Crit_Damage acv', 'skl4': 'Stun target for 2 Seconds acv'})
blind_sage = Constellation("Blind_Sage", [], {Points_of_Eldritch.name: 18, Points_of_Ascendant.name: 10},
                           [sagef, sages, saget, sageft, sageff, sagest, elemental_seeker], tier=3)

afflif = Star("Affliction", "First Affliction Star", [4, 4, 3], [Points_of_Eldritch, Points_of_Ascendant], [1, 1],
              [Points_of_Eldritch, Points_of_Ascendant, Points_of_Chaos], rank=0, Vitality_Damage=40/100,
              Poison_Damage=40/100, tier=2)
afflis = Star("Affliction", "Second Affliction Star", rank=1, Acid_Retaliation=60, Spirit=20, Offensive_Ability=20)
afflit = Star("Affliction", "Third Affliction Star", line=1, rank=3, Vitality_Damage=5, Offensive_Ability=3/100,
              to_All_Retaliation_Damage=20/100)
afflift = Star("Affliction", "Fourth Affliction Star", line=1, rank=4, Vitality_Damage=range(5, 10),
               Crit_Damage=10/100, Acid_Retaliation=60)
affliff = Star("Affliction", "Fifth Affliction Star", line=2, rank=3, Acid_Damage=50/100, Vitality_Damage=50/100,
               Acid_Retaliation=120)
afflist = Star("Affliction", "Sixth Affliction Star", line=2, rank=4, Vitality_Decay=50/100,
               to_All_Retaliation_Damage=50/100)
fetid_pool = Star("Affliction", "Fetid Pool", rank=2, Seconds_Skill_Recharge=2, Seconds_Duration=6, Meter_Radius=3,
                  of_Retaliation_Damage_added_to_Attack=7/100, Vitality_Damage=370, Poison_Damage=290,
                  Slow_Target=[30/100, 2])
affliction = Constellation("Affliction", {Points_of_Eldritch.name: 1, Points_of_Ascendant.name: 1},
                           {Points_of_Eldritch.name: 4, Points_of_Ascendant.name: 4, Points_of_Chaos.name: 3},
                           [afflif, afflis, fetid_pool, afflit, afflift, affliff, afflist], tier=2)

mogdrof = Star("Mogdrogen_The_Wolf", "First Mogdrogen The Wolf Star", [15, 12],
               [Points_of_Ascendant, Points_of_Eldritch], [0], [Points_of_Ascendant, Points_of_Eldritch], rank=0,
               Offensive_Ability=35, pets_Offensive_Ability=3/100, tier=3)
mogdros = Star("Mogdrogen_The_Wolf", "Second Mogdrogen The Wolf Star", rank=1, Bleeding_Damage=80/100,
               pets_to_All_Damage=30/100)
mogdrot = Star("Mogdrogen_The_Wolf", "Third Mogdrogen The Wolf Star", rank=2, Defensive_Ability=30,
               Vitality_Resistance=20/100, pets_Total_Speed=6/100)
mogdroft = Star("Mogdrogen_The_Wolf", "Fourth Mogdrogen The Wolf Star", rank=3, Bleeding_Damage=[54, 80/100],
                pets_Bleeding_Damage=24, of_Attack_Damage_Converted_To_Health=6/100)
mogdroff = Star("Mogdrogen_The_Wolf", "Fifth Mogdrogen The Wolf Star", rank=4, Elemental_Resistance=15/100,
                Bleeding_Resistance=15/100, Max_Bleeding_Resistance=3/100, pets_to_All_Damage=80/100)
mogdrogen_howl = Star("Mogdrogen_The_Wolf", "Howl of Mogdrogen", rank=5, Seconds_Skill_Recharge=15,
                      Seconds_Duration=10, Bleeding_Damage=[174, 275/100], Reduced_target_Defensive_Ability=144,
                      Attack_Speed=18/100, pets_Bleeding_Damage=96, pets_Offensive_Ability=15/100,
                      pets_Total_Speed=40/100)
mogdrogen_the_wolf = Constellation("Mogdrogen_The_Wolf", [],
                                   {Points_of_Ascendant.name: 15, Points_of_Eldritch.name: 12},
                                   [mogdrof, mogdros, mogdrot, mogdroft, mogdroff, mogdrogen_howl], tier=3)

rattof = Star("Rattosh_the_Veilwarden", "First Rattosh the Veilwarden Star", [10, 6, 6],
              [Points_of_Eldritch, Points_of_Chaos, Points_of_Order], [0],
              [Points_of_Eldritch, Points_of_Chaos, Points_of_Order], rank=0, Health=150, Offensive_Ability=30, tier=3)
rattos = Star("Rattosh_the_Veilwarden", "Second Rattosh the Veilwarden Star", rank=1, Vitality_Damage=80/100,
              Aether_Damage=80/100)
rattot = Star("Rattosh_the_Veilwarden", "Third Rattosh the Veilwarden Star", rank=2, Vitality_Decay=150/100,
              Offensive_Ability=45)
rattoft = Star("Rattosh_the_Veilwarden", "Fourth Rattosh the Veilwarden Star", rank=3, Vitality_Decay=54,
               Aether_Damage=100/100, Vitality_Damage=100/100)
rattoff = Star("Rattosh_the_Veilwarden", "Fifth Rattosh the Veilwarden Star", rank=4, Vitality_Damage=10,
               Pierce_Resistance=15/100, Bleeding_Resistance=15/100)
rattosh_will = Star("Rattosh_the_Veilwarden", "Will of Rattosh", rank=5, Seconds_Duration=8, Vitality_Damage=160,
                    Aether_Damage=185, Vitality_Resistance=-25/100, Life_Leech_Resistance=-8/100)
rattosh_the_veilwarden = Constellation("Rattosh_the_Veilwarden", [], {Points_of_Eldritch.name: 10,
                                                                      Points_of_Chaos.name: 6, Points_of_Order.name: 6},
                                       [rattof, rattos, rattot, rattoft, rattoff, rattosh_will], tier=3)

huntef = Star("Huntress", "First Huntress Star", [4, 4, 3], [Points_of_Eldritch, Points_of_Ascendant], [1, 1],
              [Points_of_Ascendant, Points_of_Eldritch, Points_of_Chaos], rank=0, Offensive_Ability=15, tier=3)
huntes = Star("Huntress", "Second Huntress Star", rank=1, Cunning=20, Pierce_Damage=50/100)
huntet = Star("Huntress", "Third Huntress Star", rank=2, Offensive_Ability=15, Bleeding_Damage=60/100)
hunteft = Star("Huntress", "Fourth Huntress Star", line=1, rank=3, Health=100, Damage_to_Beasts=8/100,
               Pierce_Resistance=8/100, pets_Health=8/100)
hunteff = Star("Huntress", "Fifth Huntress Star", rank=3, Offensive_Ability=3/100, pets_Offensive_Ability=5/100)
huntest = Star("Huntress", "Sixth Huntress Star", line=2, rank=4, Bleeding_Damage=[33, 50/100], pets_Bleeding_Damage=18)
rend = Star("Huntress", "Rend", line=3, rank=4, Seconds_Duration=5, Meter_Radius=5, Bleeding_Damage=285,
            Offensive_Ability=-150, Bleeding_Resistance=-32/100)
huntress = Constellation("Huntress", {Points_of_Eldritch.name: 1, Points_of_Ascendant.name: 1},
                         {Points_of_Ascendant.name: 4, Points_of_Eldritch.name: 4, Points_of_Chaos.name: 3},
                         [huntef, huntes, huntet, hunteft, hunteff, huntest, rend], tier=2)

wolvef = Star("Wolverine", "First Wolverine Star", [1], [Points_of_Ascendant], [6], [Points_of_Ascendant], rank=0,
              Defensive_Ability=15, pets_Pierce_Resistance=10/100)
wolves = Star("Wolverine", "Second Wolverine Star", rank=1, to_All_Retaliation_Damage=30/100,
              pets_Vitality_Resistance=8/100)
wolvet = Star("Wolverine", "Third Wolverine Star", rank=2, Defensive_Ability=25, pets_Poison_and_Acid_Resistance=8/100)
wolveft = Star("Wolverine", "Fourth Wolverine Star", line=1, rank=3, to_All_Retaliation_Damage=50/100,
               pets_Bleeding_Resistance=25/100)
wolveff = Star("Wolverine", "Fifth Wolverine Star", line=2, rank=3, Defensive_Ability=4/100,
               Physique_Requirement_for_Melee_Weapons=10/100, Cunning_Requirement_for_Melee_Weapons=10/100,
               pets_Defensive_Ability=5/100)
wolverine = Constellation("Wolverine", {Points_of_Ascendant.name: 6}, {str(Points_of_Ascendant.name): 1},
                          [wolvef, wolves, wolvet, wolveft, wolveff])

craf = Star("Crab", "First Crab Star", [6, 4], [Points_of_Ascendant], [3], [Points_of_Ascendant, Points_of_Order],
            rank=0, Physique=25, Constitution=15/100, tier=2)
cras = Star("Crab", "Second Crab Star", rank=1, Physical_Damage=40/100, Elemental_Damage=40/100,
            Internal_Trauma_Damage=40/100)
crat = Star("Crab", "Third Crab Star", rank=3, Defensive_Ability=55, Pierce_Resistance=18/100)
craft = Star("Crab", "Fourth Crab Star", rank=4, Elemental_Damage=[10, 40/100], Elemental_Resistance=15/100)
arcane_barrier = Star("Crab", "Arcane Barrier", rank=2, Damage_Absorbtion=2260, Seconds_Skill_Recharge=3)
crab = Constellation("Crab", {Points_of_Ascendant.name: 3}, {Points_of_Ascendant.name: 6, Points_of_Order.name: 4},
                     [craf, cras, crat, craft, arcane_barrier], tier=2)

boaf = Star("Autumn_Boar", "First Autumn Boar Star", [4, 4, 3], [Points_of_Ascendant], [3],
            [Points_of_Primordial, Points_of_Ascendant, Points_of_Order], rank=0, Physique=20, Cunning=20,
            to_All_Retaliation_Damage=25/100, tier=2)
boas = Star("Autumn_Boar", "Second Autumn Boar Star", rank=1, Physique=15, Pierce_Resistance=15/100)
boat = Star("Autumn_Boar", "Third Autumn Boar Star", rank=2, Physique=5/100, to_All_Retaliation_Damage=25/100)
boaft = Star("Autumn_Boar", "Fourth Autumn Boar Star", line=1, rank=3, Physical_Resistance=4/100, Defensive_Ability=25)
boaff = Star("Autumn_Boar", "Fifth Autumn Boar Star", rank=3, Defensive_Ability=30, to_All_Retaliation_Damage=25/100)
boast = Star("Autumn_Boar", "Sixth Autumn Boar Star", line=2, rank=4, Physical_Damage_Retaliation=150,
             Reflected_Damage_Reduction=10/100)
trample = Star("Autumn_Boar", "Trample", line=3, rank=4, Seconds_Skill_Recharge=0.3, Meter_Radius=0.1,
               Chance_to_pass_through_Enemies=100/100, Weapon_Damage=55/100,
               of_Retaliation_Damage_added_to_Attack=14/100, Internal_Trauma_Damage=570, Knockdown=0)
autumn_boar = Constellation("Autumn_Boar", {Points_of_Ascendant.name: 3},
                            {Points_of_Primordial.name: 4, Points_of_Ascendant.name: 4, Points_of_Order.name: 3},
                            [boaf, boas, boat, boaft, boaff, boast, trample], tier=2)

rhowaf = Star("Rhowans_Scepter", "First Rhowans Scepter Star", [6, 4], [Points_of_Ascendant, Points_of_Order], [3, 2],
              [Points_of_Ascendant, Points_of_Order], rank=0, Defensive_Ability=20, tier=2)
rhowas = Star("Rhowans_Scepter", "Second Rhowans Scepter Star", rank=1, Health=6/100)
rhowat = Star("Rhowans_Scepter", "Third Rhowans Scepter Star", line=1, rank=2, Defensive_Ability=30, Armor=40)
rhowaft = Star("Rhowans_Scepter", "Fourth Rhowans Scepter Star", line=2, rank=2, Physical_Damage=50/100,
               Reduced_Petrify_Duration=25/100)
rhowaff = Star("Rhowans_Scepter", "Fifth Rhowans Scepter Star", line=2, rank=3, Internal_Trauma_Damage=[50, 80/100])
rhowast = Star("Rhowans_Scepter", "Sixth Rhowans Scepter Star", line=1, rank=3, Internal_Trauma_Damage=[75, 50/100])
rhowans_scepter = Constellation("Rhowans_Scepter", {Points_of_Ascendant.name: 3, Points_of_Order.name: 2},
                                {Points_of_Ascendant.name: 6, Points_of_Order.name: 4},
                                [rhowaf, rhowas, rhowat, rhowaft, rhowaff, rhowast], tier=2)

olerof = Star("Oleron", "First Oleron Star", [20, 7], [Points_of_Ascendant, Points_of_Order], [0],
              [Points_of_Ascendant, Points_of_Order], rank=0, Physique=30, Cunning=30, Health=100, tier=3)
oleros = Star("Oleron", "Second Oleron Star", rank=1, Physical_Damage=80/100, Internal_Trauma_Damage=80/100,
              Bleeding_Damage=80/100)
olerot = Star("Oleron", "Third Oleron Star", rank=2, Offensive_Ability=30, Armor=80, Bleeding_Resistance=10/100)
oleroft = Star("Oleron", "Fourth Oleron Star", rank=3, Health=200, Physical_Resistance=4/100)
oleroff = Star("Oleron", "Fifth Oleron Star", line=1, rank=4, Internal_Trauma_Damage=[90, 100/100],
               Offensive_Ability=15, Maximum_Pierce_Resistance=2/100)
olerost = Star("Oleron", "Sixth Oleron Star", line=2, rank=4, Physical_Damage=[range(11, 13), 100/100],
               Bleeding_Damage=100/100)
blind_fury = Star("Oleron", "Blind Fury", line=3, rank=4, Seconds_Skill_Recharge=1, Meter_Target_Area=5,
                  Weapon_Damage=75/100, Physical_Damage=155, Internal_Trauma_Damage=580, Bleeding_Damage=580,
                  Slower_Enemy_Attack=30/100)
oleron = Constellation('Oleron', [], {Points_of_Ascendant.name: 20, Points_of_Order.name: 7},
                       [olerof, oleros, olerot, oleroft, oleroff, olerost, blind_fury], tier=3)

leviaf = Star("Leviathan", "First Leviathan Star", [13, 13], [Points_of_Eldritch, Points_of_Ascendant], [0],
              [Points_of_Eldritch, Points_of_Ascendant], rank=0, Cold_Damage=[6, 80/100], tier=3)
levias = Star("Leviathan", "Second Leviathan Star", rank=1, Physique=35, Health=5/100)
leviat = Star("Leviathan", "Third Leviathan Star", rank=2, Energy=10/100, Defensive_Ability=40,
              Increases_Energy_Regeneration=20/100)
leviaft = Star("Leviathan", "Fourth Leviathan Star", rank=3, Pierce_Resistance=20/100, Physical_Resistance=4/100)
leviaff = Star("Leviathan", "Fifth Leviathan Star", line=1, rank=4, Frostburn_Damage=[45, 100/100],
               Maximum_Cold_Resistance=3/100)
leviast = Star("Leviathan", "Sixth Leviathan Star", line=2, rank=4, Cold_Damage=[range(8, 10), 100/100])
whirpool = Star("Leviathan", "Whirpool", line=3, rank=4, Seconds_Skill_Recharge=2, Seconds_Duration=6, Meter_Radius=3.5,
                Cold_Damage=420, Frostburn_Damage=340, Slower_target_Movement=40/100)
leviathan = Constellation("Leviathan", [], {str(Points_of_Eldritch.name): 13, str(Points_of_Ascendant.name): 13},
                          [leviaf, levias, leviat, leviaft, leviaff, leviast, whirpool], tier=3)

seruf = Star("Attak_Seru_The_Mirage", "First Attak Seru The Mirage Star", [16, 14],
             [Points_of_Ascendant, Points_of_Eldritch], [0], [Points_of_Ascendant, Points_of_Eldritch], rank=0,
             Defensive_Ability=25, Aether_Damage=80/100, tier=3)
serus = Star("Attak_Seru_The_Mirage", "Second Attak Seru The Mirage Star", rank=1, Elemental_Damage=80/100,
             Defensive_Ability=25)
serut = Star("Attak_Seru_The_Mirage", "Third Attak Seru The Mirage Star", rank=2, Pierce_Resistance=25/100,
             Bleeding_Resistance=25/100)
seruft = Star("Attak_Seru_The_Mirage", "Fourth Attak Seru The Mirage Star", rank=3, Defensive_Ability=4/100,
              Health=300)
seruff = Star("Attak_Seru_The_Mirage", "Fifth Attak Seru The Mirage Star", line=1, rank=4,
              Elemental_Damage=[13, 100/100], Aether_Damage=100/100)
arcane_currents = Star("Attak_Seru_The_Mirage", "Arcane Currents", line=2, rank=4, Seconds_Skill_Recharge=1,
                       Summon_Limit=5,
                       Arcane_Current_Attributes={'attr1': 'Lives_for 4.5 attr', 'attr2': '7448 Health attr',
                                                  'attr3': '300 Energy attr'},
                       Surge={'skl1': '14 Meter_Range skl', 'skl2': '235 Elemental Damage skl',
                              'skl3': '235 Aether Damage skl', 'skl4': '40% Crit Damage skl'})
attak_seru_the_mirrage = Constellation("Attak_Seru_The_Mirage", [],
                                       {Points_of_Ascendant.name: 16, Points_of_Eldritch.name: 14},
                                       [seruf, serus, serut, seruft, seruff, arcane_currents], tier=3)

# List of all stars, used in variety of operations.
stars_list = [cschaos, csasc, csord, csprim, cseld, tortof, tortos, tortot, tortoft, turtle_shell, sailof, sailos,
              sailot, sailoft, tsunaf, tsunas, tsunat, tsunaft, tsunami_skill, impf, imps, impt, impft, aetherfire,
              falcof, falcos, falcot, falcoft, falcon_swoop, ratf, rats, ratt, ratft, cranef, cranes, cranet, craneft,
              craneff, liof, lios, liot, bullf, bulls, bullt, bullft, bull_rush, hounf, houns, hount, scaraf, scaras,
              scarat, scaraft, gallof, gallos, gallot, galloft, lizaf, lizas, lizat, vipef, vipes, vipet, vipeft,
              jackaf, jackas, jackat, wref, wres, wret, wreft, batf, bats, batt, batft, twin_fangs, geyef, geyes,
              geyet, geyeft, guardians_gaze, guardians_gaze, akerof, akeros, akerot, akeroft, scorpion_sting,
              scorpion_sting, shepf, sheps, shept, shepft, shepherd_call, shepherd_call, talof, talos, talot, taloft,
              anvif, anvis, anvit, anvift, targo_hammer, hamef, hames, hamet, bassaf, bassas, bassat, bassaft,
              assassin_mark, assaf, assas, assat, assaft, assaff, assast, blades_of_wrath, dryaf, dryas, dryat, dryaft,
              dryads_blessing, eelf, eels, eelt, panthef, panthes, panthet, pantheft, staf, stas, stat, staft, srattof,
              srattos, srattot, srattoft, srattoff, srattost, widof, widos, widot, widoft, widoff, arcane_bomb, krakef,
              krakes, kraket, krakeft, krakeff, wraif, wrais, wrait, wraift, tempef, tempes, tempet, tempeft, tempeff,
              tempestc, reckless_tempest, vultuf, vultus, vultut, vultuft, vultuff, fief, fies, fiet, fieft,
              flame_torrent, ghouf, ghous, ghout, ghouft, ghoulish_hunger, spidef, spides, spidet, spideft, spideff,
              ravef, raves, ravet, raveft, quif, quis, quitt, quift, lschof, lschos, lschot, hawkf, hawks, hawkt, owlf,
              owls, owlt, owlft, harpyf, harpys, harpyt, harpyft, tarbuf, tarbus, tarbut, tarbuft, tarbuff, tarbust,
              shield_wall, bnadaf, bnadas, bnadat, bnadaft, bnadaff, bnadast, uscaf, uscas, uscat, uscaft, uscaff,
              tip_scales, wsolef, wsoles, wsolet, wsoleft, wsoleff, lotuf, lotusc, lotut, lotuft, bdiref, bdires,
              bdiret, bdireft, bdireff, maul, amatof, amatos, amatot, amatoft, amatoff, amatost, blizzard, hspeaf,
              hspeas, hspeat, hspeaft, hspeaff, heavens_spear, wmessef, wmesses, wmesset, wmesseft, wmesseff,
              war_messenger, dchariof, dcharios, dchariot, dcharioft, dcharioff, dchariost, wayward_soul, mantif,
              mantisc, mantit, mantift, wsolaef, wsolaes, wsolaet, wsolaeft, eldritch_fire, bersef, berses, berset,
              berseft, berseff, bersest, bysmief, bysmies, bysmiet, bysmieft, bysmiels_command, foxf, foxs, foxt, foxft,
              manticof, manticos, manticot, manticoft, manticoff, acid_spray, sharvef, sharves, sharvet, sharveft,
              sharveff, sharvest, ethrof, ethros, ethrot, ethroft, rcrof, rcros, rcrot, rcroft, elemental_storm, toadf,
              toads, toadt, toadft, typhof, typhos, typhot, typhoft, typhoff, typhost, ulzaaf, ulzaas, ulzaat, ulzaaft,
              ulzaaff, ulzaads_decree, usoldief, usoldies, usoldiet, usoldieft, usoldieff, usoldiest,
              unknown_soldier_skill, barhaf, barhas, barhat, barhaft, barhaff, inspiration, azraaf, azraas, azraat,
              azraaft, azraaff, shifting_sands, shief, shies, shiet, shieft, shieff, shiest, ulof, ulos, ulot, uloft,
              cleansing_waters, menhif, menhis, menhit, menhift, menhiff, menhist, stone_form, empyriof, empyrios,
              empyriot, empyrioft, empyrioff, empyriost, empyrions_light, ishtaf, ishtas, ishtat, ishtaft, ishtaff,
              natures_guardians, treef, trees, treet, treeft, treeff, healing_rain, korvaf, korvas, korvat, korvaft,
              korvaff, korvak_eye, viref, vires, viret, vireft, vireff, vire_fist, aeof, aeos, aeot, aeoft, aeoff,
              time_dilation, revef, reves, revet, reveft, reveff, raise_dead, dygof, dygos, dygot, dygoft, dygoff,
              dygost, hungering_void, yugof, yugos, yugot, yugoft, yugoff, yougol_blood, wendif, wendis, wendit,
              wendift, wendiff, wendigos_mark, hydraf, hydras, hydrat, hydraft, hydraff, hydrast, ulzuf, ulzus, ulzut,
              ulzuft, ulzuff, ulzust, meteor_shower, hyriaf, hyrias, hyriat, hyriaft, hyriaff, hyrians_glare, magif,
              magis, magit, magift, magiff, magist, fissure, lantef, lantes, lantet, lanteft, lanteff, behef, behes,
              behet, beheft, beheff, giants_blood, abomif, abomis, abomit, abomift, abomiff, abomist, abominable_might,
              tainted_eruption, murmuf, murmus, murmut, murmuft, murmuff, rumor, alladraf, alladras, alladrat,
              alladraft, phoenix_fire, ultof, ultos, ultot, ultoft, ultoff, ultos_hand, sagef, sages, saget, sageft,
              sageff, sagest, elemental_seeker, afflif, afflis, afflit, afflift, affliff, afflist, fetid_pool, mogdrof,
              mogdros, mogdrot, mogdroft, mogdroff, mogdrogen_howl, rattof, rattos, rattot, rattoft, rattoff,
              rattosh_will, huntef, huntes, huntet, hunteft, hunteff, huntest, rend, wolvef, wolves, wolvet, wolveft,
              wolveff, craf, cras, crat, craft, arcane_barrier, boaf, boas, boat, boaft, boaff, boast, trample, rhowaf,
              rhowas, rhowat, rhowaft, rhowaff, rhowast, olerof, oleros, olerot, oleroft, oleroff, olerost, blind_fury,
              leviaf, levias, leviat, leviaft, leviaff, leviast, whirpool, seruf, serus, serut, seruft, seruff,
              arcane_currents]
constellations = [tsunami, scholars_light, crossroads_of_ascendant, crossroads_of_chaos, crossroads_of_eldritch,
                  crossroads_of_order, crossroads_of_primordial, attak_seru_the_mirrage, dryad, assassin, rat, crane,
                  lion, gallows, lizard, viper, jackal, wretch, bat, eye_of_the_guardian, akerons_scorpion,
                  shepherds_crook, nightallon, assassins_blade, eel, panther, stag, rattosh_staff, widow, kraken,
                  wraith, tempest, vulture, fiend, ghoul, spider, raven, quill, hawk, owl, harpy, targo_the_builder,
                  blades_of_nadan, schales_of_ulcana, lotus, amatok_the_spirit_of_winter, spear_of_the_heavens,
                  messenger_of_war, chariot_of_the_dead, solaels_witchblade, berserker, bysmiels_bonds, fox, manticore,
                  harvestmans_scythe, empty_throne, rhowans_crown, toad, typhos_the_jailor_of_souls,
                  ulzaad_herald_of_korvak, unknown_soldier, bards_harp, shieldmaiden, ulo_the_keeper_of_the_waters,
                  light_of_empyrion, ishtak_the_spring_maiden, tree_of_life, korvak_the_eldritch_sun, aeons_hourglass,
                  revenant, dying_god, yugol_the_insatiable_night, wendigo, hydra, ulzuins_torch,
                  hyrian_guardian_of_the_celestial_gates, magi, oklaines_lantern, abomination,
                  murmur_mistress_of_rumors, alladrahs_phoenix, hand_of_ultos, blind_sage, affliction,
                  mogdrogen_the_wolf, rattosh_the_veilwarden, huntress, wolverine, crab, autumn_boar, leviathan,
                  sailor_guide, falcon, imp, tortoise, bull, hound, scarab, anvil, hammer, solemn_watcher, dire_bear,
                  mantis, azraaka_the_eternal_sands, obelisk_of_menhir, vire_the_stone_matron, behemoth,
                  rhowans_scepter, oleron]

locked_stars = []

crossroads_list = [crossroads_of_order, crossroads_of_ascendant, crossroads_of_primordial, crossroads_of_eldritch,
                   crossroads_of_chaos]


def standard_mode(st):
    """
    Attempts to unlock a star while keeping to the in-game mechanics.
    :param st: A star to unlock.
    :return: The list of unlocked stars.
    """
    if Devotion_Points_Pool.devpoints > 0:
        st.check_requirement()

    return unlocked_stars


def standard_mode_lock(st):
    """
    Attempts to lock a star while keeping to the in-game mechanics.
    :param st: A star to lock.
    :return: The list of unlocked stars.
    """
    if type(st) == Constellation:
        st = st.members[0]
    if 'Crossroads' in st.name:
        st.lock(len(st.bonus_type))
    else:
        st.lock(len(st.find_constellation().members[0].bonus_type))
    return unlocked_stars


def update_bonus_pool(bonus):
    """
    Sump up values of a particular bonus.
    :param bonus: A particular bonus from attributes_dict.
    :return: A tuple with percentage and fat bonus.
    """
    percentage_bonus = 0
    flat_bonus = 0
    for i in attributes_dict[bonus]:
        if i:
            if type(i) == float:
                percentage_bonus += i
            if type(i) == range:
                convert = mean([i[0], i[1]])
                flat_bonus += convert
            if type(i) == int:
                flat_bonus += i
            if type(i) == str:
                percentage_bonus += float(i.strip('%'))/100

    return percentage_bonus, flat_bonus


def find_possibilities(aff, after_rare=False, rare=None, rare_contribution=0):
    """

    :param aff:
    :param after_rare:
    :param rare:
    :param rare_contribution:
    :return:
    """
    result = []
    size = None
    if rare == 1:
        rare = 2
    if type(star) == Star:
        base_requirement = star.find_constellation().requirement[aff] - rare_contribution
    else:
        base_requirement = star.requirement[aff] - rare_contribution

    number = base_requirement
    if aff == Points_of_Order.name or aff == Points_of_Chaos.name:
        if base_requirement >= 8:
            size = 3
        elif 7 >= base_requirement > 5:
            size = 2
        elif base_requirement <= 5 and base_requirement != 4:
            size = 1
        elif base_requirement == 4:
            size = 2
    elif aff == Points_of_Ascendant.name or aff == Points_of_Eldritch.name:
        if base_requirement >= 17:
            size = 4
        elif 17 > base_requirement >= 12:
            size = 3
        elif 12 > base_requirement > 6:
            size = 2
        else:
            size = 1
    elif aff == Points_of_Primordial.name:
        if base_requirement >= 16:
            size = 4
        elif 16 > base_requirement >= 11:
            size = 3
        elif 11 > base_requirement > 5:
            size = 2
        else:
            size = 1
    if after_rare and rare:
        for i in sum_to_n(rare, size):
            result.append(dict({aff: i}))
    else:
        for i in sum_to_n(number, size):
            result.append(dict({aff: i}))
    return result


def find_rare_possibilities(aff, st):
    """
    Some constellations give a bonus to two types of affinity. Therefore in some rare cases unlocking such a
    constellation is a better choice even if it takes more devotion points.
    :param aff: Affinity type.
    :param st: A star to unlock.
    :return: A list of dictionaries. One dictionary contains affinity name as key and numbers representing affinity
    requirement for the star.
    """
    result = []
    size = None
    if type(st) == Star:
        const = st.find_constellation()
    else:
        const = st

    number = const.requirement[aff]
    if aff == Points_of_Order.name or aff == Points_of_Chaos.name:
        if const.requirement[aff] >= 8:
            size = 4
        elif 7 >= const.requirement[aff] > 5:
            size = 3
        elif const.requirement[aff] <= 5:
            size = 2
        elif const.requirement[aff] == 2:
            size = 1
    elif aff == Points_of_Ascendant.name or aff == Points_of_Eldritch.name:
        if const.requirement[aff] >= 17:
            size = 5
        elif 17 > const.requirement[aff] >= 12:
            size = 4
        elif 12 > const.requirement[aff] > 6:
            size = 3
        else:
            size = 1
    elif aff == Points_of_Primordial.name:
        if const.requirement[aff] >= 16:
            size = 5
        elif 16 > const.requirement[aff] >= 11:
            size = 4
        elif 11 > const.requirement[aff] > 5:
            size = 3
        else:
            size = 1
    for i in sum_to_n(number, size):
        result.append(dict({aff: i}))

    return result


def sum_to_n(number, size, limit=None):
    """
    The function found on stack overflow. It finds all possible ways to sum up to a number, e.g. 6 given the 'size' that
    is how many integers should be summed up. For example, if the number is 6 and size is 2, the return values will be:
    [2, 4], [3, 3], [5, 1].
    :param number: n to sum up to.
    :param size: How many integers to sum.
    :param limit: It is defined by number parameter.
    :return: A return values is appended to the result of the find_possibilities functions.
    """
    """Produce all lists of `size` positive integers in decreasing order
    that add up to `n`."""
    # Size 1 means that one constellation with an affinity bonus of 'number' will be enough to meet one of the star's
    # requirements.
    if size == 1:
        yield [number]
        return
    if limit is None:
        limit = number
    start = (number + size - 1) // size
    stop = min(limit, number - size + 1) + 1
    for i in range(start, stop):
        # there is no constellation with affinity bonus higher than 6.
        if i > 6:
            break
        for tail in sum_to_n(number - i, size - 1, i):
            yield [i] + tail


def add_up_members(selection_list):
    """
    The function calculates number of devotion points needed to unlock a set of constellations(selection_list)
    :param selection_list: A list of lists. One list contain a set of constellations.
    :return: selection_list with a number of devotion points at index -1 of each list.
    """
    for selection in selection_list:
        counter = 0
        if crossroads_of_chaos not in selection and crossroads_of_eldritch not in selection and \
                crossroads_of_primordial not in selection and crossroads_of_ascendant not in selection \
                and crossroads_of_order not in selection:
            counter -= 1
        for constellation in selection:
            counter += len(constellation.members)
        selection.append(counter)
    return selection_list


def create_possibilities(poss_list, aff, second):
    """
    The function creates possibility objects.
    :param poss_list: The method to be examined. Rare, standard or mixed.
    :param aff: The first or secend affinity.
    :param second: The second or third affinity.
    :return: A list of possibilities.
    """
    result = []
    for i in poss_list:
        i = Possibility(str(i), i, aff, secondary=second)
        result.append(i)
        i.define_variety()
    return result


def choose_best(picks, affinity_number, standard, rare=None, mixed=None, rare_two=None, rare_three=None):
    """
    Calculates which of the ways of unlocking constellations takes least devotion points.
    :param picks: A list of methods(rare, standard, mixed).
    :param affinity_number: Number of affinity requirements.
    :param standard: The standard method.
    :param rare: The rare method.
    :param mixed: The mixed method.
    :param rare_two: Another variation of rare method.
    :param rare_three: Another variation of rare method.
    :return: The variation which takes the least devotion points to unlock.
    """
    if affinity_number == 1:
        best = min(standard.calculate_devpoints(1), rare.calculate_devpoints(1), mixed.calculate_devpoints(1))
    elif affinity_number == 2:
        best = min(standard.calculate_devpoints(2), rare.calculate_devpoints(2), mixed.calculate_devpoints(2))
    else:
        best = min(standard.calculate_devpoints(3), rare.calculate_devpoints(3), rare_two.calculate_devpoints(3),
                   rare_three.calculate_devpoints(3))
    for i in picks:
        if i and best == i.calculate_devpoints(affinity_number):
            best = i
    return best.merged


star = None
const_affinity_bonus = None


def fast_mode(clicked_star):
    """
    Unlock a star that has been clicked using as little devotion points as possible.
    :param clicked_star: A star that has been clicked by an app user.
    :return: A list with all unlocked stars.
    """

    second_related_affinity = None
    third_related_affinity = None
    global star
    star = clicked_star
    stars_constellation = star.find_constellation()

    for i in stars_constellation.requirement:
        if type(stars_constellation.requirement[i]) == list:
            stars_constellation.requirement[i] = stars_constellation.requirement[i][0]
    # Unlock the clicked star if its affinity requirements have already been met.
    if stars_constellation.update_status():
        stars_constellation.unlock_till_star(star)
        split_stars = [x.name.replace(' ', '') for x in unlocked_stars]
        return split_stars
    # Otherwise meet the affinity requirements using as little devotion points as possible.
    else:
        list(map(lambda a: a.unlock_fast(), crossroads_list))
        current_requirement = stars_constellation.update_requirement()
        related_affinity = []
        list(map(lambda a: a.update_unlock_status() if type(a) != int else None, crossroads_list))

        for affinity in affinities:
            if affinity.name in stars_constellation.requirement:
                related_affinity.append(affinity.name)
        if len(current_requirement) == 1:
            first_related_affinity = list(current_requirement.keys())[0]
            global const_affinity_bonus
            const_affinity_bonus = [x for x in constellations for affinity in x.affinity_bonus if
                                    affinity == first_related_affinity and x.tier == 1]
            const_affinity_bonus_unlockable = [x for x in const_affinity_bonus if x.update_status()]

            if type(stars_constellation.requirement[first_related_affinity]) == list and \
                    len(stars_constellation.requirement[first_related_affinity]) > 1:
                stars_constellation.requirement[first_related_affinity].pop()
                stars_constellation.requirement[first_related_affinity] = \
                    int(stars_constellation.requirement[first_related_affinity])

            # Now determine all possible ways to meet the star requirement.
            standard_possibilities = find_possibilities(first_related_affinity)
            # Create objects for every possible way. The object represents a set of constellations which need to be
            # unlocked
            # to reach the desired star.
            standard_ps = create_possibilities(standard_possibilities, first_related_affinity, second_related_affinity)

            # Create lists with constellations which give affinity bonus to searched affinity types.
            # Option = constellation.
            list(map(lambda a: a.update_options(const_affinity_bonus_unlockable, a.affinity,
                                                second_related_affinity, third_related_affinity), standard_ps))
            # Find constellations for each set of possibility.
            standard_selection = list(map(lambda a: a.update_selected(a.affinity), standard_ps))
            standard_selection = [x for x in standard_selection if x]
            # Let's calculate how many devotion points are needed to unlock a given list of constellations.
            add_up_members(standard_selection)
            # Pick a list of constellations with the lowest number of devotion points required.
            standard_pick = min(standard_selection, key=lambda a: a[-1])
            # Create a FastMode object. It will facilitate the process of finding the fastest possible way to unlock a
            # desired star.
            final_result = standard_pick
        # If the star has two types of affinity requirement the program needs to determine each one of them.
        elif len(current_requirement) == 2:
            first_related_affinity = list(current_requirement.keys())[0]
            second_related_affinity = list(current_requirement.keys())[1]
            third_related_affinity = 'gowno'
            if type(stars_constellation.requirement[first_related_affinity]) == list and \
                    len(stars_constellation.requirement[first_related_affinity]) > 1:

                stars_constellation.requirement[first_related_affinity].pop()
                stars_constellation.requirement[first_related_affinity] = \
                    stars_constellation.requirement[first_related_affinity][0]
            if type(stars_constellation.requirement[second_related_affinity]) == list \
                    and len(stars_constellation.requirement[second_related_affinity]) > 1:

                stars_constellation.requirement[second_related_affinity].pop()
                stars_constellation.requirement[second_related_affinity] = \
                    stars_constellation.requirement[second_related_affinity][0]

            const_affinity_bonus = [x for x in constellations for affinity in x.affinity_bonus if affinity
                                    == first_related_affinity or affinity == second_related_affinity and x.tier == 1]
            const_affinity_bonus_unlockable = [x for x in const_affinity_bonus if x.update_status()]
            # Now determine all possible ways to meet the star requirement.
            rare_possibilities = find_rare_possibilities(first_related_affinity, star)
            standard_possibilities = find_possibilities(first_related_affinity, star)
            standard_possibilities_two = find_possibilities(second_related_affinity, star)

            # Create objects for every possible way. The object represents a set of constellations which need to be
            # unlocked
            # to reach the desired star.
            rare_ps = create_possibilities(rare_possibilities, first_related_affinity, second_related_affinity)
            standard_ps = create_possibilities(standard_possibilities, first_related_affinity, second_related_affinity)
            standard_ps_two = create_possibilities(standard_possibilities_two, second_related_affinity,
                                                   second_related_affinity)
            # Below block of code removes constellations which have two types of affinity bonus but they do not match
            # both searched affinities(first_related_affinity and second_related_affinity)
            for i in const_affinity_bonus_unlockable:
                if len(i.affinity_bonus) > 1 and second_related_affinity not in i.affinity_bonus:
                    const_affinity_bonus_unlockable.remove(i)
            # Create lists with constellations which give affinity bonus to searched affinity types.
            # Option = constellation.
            list(map(lambda a: a.update_options(const_affinity_bonus_unlockable, a.affinity,
                                                second_related_affinity, third_related_affinity), rare_ps))
            list(map(lambda a: a.update_options(const_affinity_bonus_unlockable, a.affinity,
                                                second_related_affinity, third_related_affinity), standard_ps))
            list(map(lambda a: a.update_options(const_affinity_bonus_unlockable, a.affinity,
                                                second_related_affinity, third_related_affinity), standard_ps_two))
            # Find constellations for each set of possibility.
            rare_selection = list(map(lambda a: a.update_selected(a.affinity), rare_ps))
            rare_selection = [x for x in rare_selection if x]
            standard_selection = list(map(lambda a: a.update_selected(a.affinity), standard_ps))
            standard_selection = [x for x in standard_selection if x]
            second_standard_selection = list(map(lambda a: a.update_selected(a.affinity), standard_ps_two))
            second_standard_selection = [x for x in second_standard_selection if x]
            # Mixed selection combines standard and rare method. If a standard_selection contains a constellation
            # which give
            # bonus to two searched affinity types, the program will calculate a new value for the second list of
            # possibility sets. This method though does not use a greater 'size' for a possibility set like the rare
            # method does.
            mixed_selection = []
            for i in standard_selection:
                for item in i:
                    if len(
                            item.affinity_bonus) > 1 and first_related_affinity in item.affinity_bonus \
                            and second_related_affinity in item.affinity_bonus:
                        mixed_selection.append(i)
            # Let's calculate how many devotion points are needed to unlock a given list of constellations.
            add_up_members(rare_selection)
            add_up_members(standard_selection)
            add_up_members(second_standard_selection)
            # Pick a list of constellations with the lowest number of devotion points required.
            standard_pick = min(standard_selection, key=lambda a: a[-1])
            second_standard_pick = min(second_standard_selection, key=lambda a: a[-1])
            rare_pick = min(rare_selection, key=lambda a: a[-1])
            # Create a FastMode object. It will facilitate the process of finding the fastest possible way to unlock a
            # desired star.
            rare_method = FastMode(star.name, rare_pick, first_related_affinity, secondary=second_related_affinity)
            standard_method = FastMode(star.name, standard_pick, first_related_affinity, poss_two=second_standard_pick,
                                       secondary=second_related_affinity)
            # Create a default rare method object.
            mixed_method = FastMode(star.name, 0, first_related_affinity, secondary=second_related_affinity)
            # Thanks to a two-affinity-bonus constellation(s) included in the best_pick along with the first affinity
            # requirement met there is also some points put into the second requirement. The program now evaluates
            # how many affinity points there is left to unlock and stores it in the rare_included variable.
            rare_included = rare_method.evaluate_secondary_points(rare_method.secondary, rare_method.poss_one)
            # Find all possible constellations sets to unlock based on rare_included number.
            rare_contribution = stars_constellation.see_missing_points(requir=second_related_affinity)[
                                    second_related_affinity] - rare_included
            if rare_contribution == 0:
                rare_method = FastMode(star.name, 0, first_related_affinity, secondary=second_related_affinity)
            else:
                rare_match_possibilities = find_possibilities(second_related_affinity, after_rare=True,
                                                              rare=rare_included,
                                                              rare_contribution=rare_contribution)
                rare_ps_two = create_possibilities(rare_match_possibilities, second_related_affinity,
                                                   second_related_affinity)

                # Set up the second selection list for the rare method
                second_rare_selection = list(map(lambda a: a.update_options(const_affinity_bonus_unlockable,
                                                 second_related_affinity, second_related_affinity,
                                                 third_related_affinity), rare_ps_two))
                second_rare_selection = list(map(lambda a: a.update_selected(second_related_affinity), rare_ps_two))
                second_rare_selection = [x for x in second_rare_selection if x]
                add_up_members(second_rare_selection)
                # Pick the list with the lowest requirement needed.
                second_rare_pick = min(second_rare_selection, key=lambda a: a[-1])
                # update the FastMode object with the pick
                rare_method.update_poss(poss_two=second_rare_pick)
                # Combine the first pick with the second so that the total number of devotion points required can be
                # calculated.
                rare_method.merge_possibilities()
            standard_method.merge_possibilities()
            # The rare method can't always be created. In such case, the default mixed method object was created.
            # If it gets created, the whole process known from standard and rare method needs to be applied.
            if mixed_selection:
                mixed_pick = min(mixed_selection, key=lambda a: a[-1])
                mixed_method = FastMode(star.name, mixed_pick, first_related_affinity,
                                        secondary=second_related_affinity)
                mixed_included = mixed_method.evaluate_secondary_points(mixed_method.secondary, mixed_method.poss_one)
                mixed_contribution = star.find_constellation().see_missing_points(requir=second_related_affinity)[
                    second_related_affinity] - mixed_included
                mixed_match_possibilities = find_possibilities(second_related_affinity, after_rare=True,
                                                               rare=mixed_included,
                                                               rare_contribution=mixed_contribution)
                mixed_ps = create_possibilities(mixed_match_possibilities, second_related_affinity,
                                                second_related_affinity)
                mixed_selection = list(map(lambda a: a.update_options(const_affinity_bonus_unlockable,
                                           second_related_affinity, second_related_affinity,
                                           third_related_affinity), mixed_ps))
                mixed_selection = list(map(lambda a: a.update_selected(second_related_affinity), mixed_ps))
                mixed_selection = [x for x in mixed_selection if x]
                add_up_members(mixed_selection)
                second_mixed_pick = min(mixed_selection, key=lambda a: a[-1])
                mixed_method.update_poss(poss_two=second_mixed_pick)

            # The program now calculates which method requires the least devotion points to unlock the searched star.
            final_result = choose_best([standard_method, rare_method, mixed_method], 2, standard_method,
                                       rare=rare_method, mixed=mixed_method)

        elif len(current_requirement) == 3:
            first_related_affinity = list(current_requirement.keys())[0]
            second_related_affinity = list(current_requirement.keys())[1]
            third_related_affinity = list(current_requirement.keys())[2]

            const_affinity_bonus = [x for x in constellations for affinity in x.affinity_bonus if
                                    affinity == first_related_affinity or affinity == second_related_affinity
                                    or affinity == third_related_affinity and x.tier == 1]
            const_affinity_bonus_unlockable = [x for x in const_affinity_bonus if x.update_status()]
            # Now determine all possible ways to meet the star requirement.
            rare_aff_one = find_rare_possibilities(first_related_affinity, star)
            rare_aff_two = find_rare_possibilities(second_related_affinity, star)
            rare_aff_three = find_rare_possibilities(third_related_affinity, star)
            standard_aff_one = find_possibilities(first_related_affinity)
            standard_aff_two = find_possibilities(second_related_affinity)
            standard_aff_three = find_possibilities(third_related_affinity)
            # Create objects for every possible way. The object represents a set of constellations which need to be
            # unlocked
            # to
            # reach the desired star.
            rare_aff_one = create_possibilities(rare_aff_one, first_related_affinity, second_related_affinity)
            rare_aff_two = create_possibilities(rare_aff_two, second_related_affinity, second_related_affinity)
            rare_aff_three = create_possibilities(rare_aff_three, third_related_affinity, second_related_affinity)
            standard_aff_one = create_possibilities(standard_aff_one, first_related_affinity, second_related_affinity)
            standard_aff_two = create_possibilities(standard_aff_two, second_related_affinity, second_related_affinity)
            standard_aff_three = create_possibilities(standard_aff_three, third_related_affinity,
                                                      second_related_affinity)
            # Below block of code removes constellations which have two types of affinity bonus but they do not match
            # both searched affinities(first_related_affinity and second_related_affinity or third_related_affinity)

            for i in const_affinity_bonus_unlockable:
                if len(i.affinity_bonus) > 1:
                    for aff in i.affinity_bonus:
                        if aff not in [second_related_affinity, third_related_affinity, first_related_affinity]:
                            const_affinity_bonus_unlockable.remove(i)
            for i in const_affinity_bonus_unlockable:
                if len(i.affinity_bonus) > 1:
                    for aff in i.affinity_bonus:
                        if aff not in [second_related_affinity, third_related_affinity, first_related_affinity]:
                            const_affinity_bonus_unlockable.remove(i)

            # Create lists with constellations which give affinity bonus to searched affinity types.
            # Option = constellation.
            list(map(lambda a: a.update_options(const_affinity_bonus_unlockable, a.affinity,
                                                second_related_affinity, third_related_affinity), rare_aff_one))
            list(map(lambda a: a.update_options(const_affinity_bonus_unlockable, a.affinity,
                                                second_related_affinity, third_related_affinity), rare_aff_two))
            list(map(lambda a: a.update_options(const_affinity_bonus_unlockable, a.affinity,
                                                second_related_affinity, third_related_affinity), rare_aff_three))
            list(map(lambda a: a.update_options(const_affinity_bonus_unlockable, a.affinity,
                                                second_related_affinity, third_related_affinity), standard_aff_one))
            list(map(lambda a: a.update_options(const_affinity_bonus_unlockable, a.affinity,
                                                second_related_affinity, third_related_affinity), standard_aff_two))
            list(map(lambda a: a.update_options(const_affinity_bonus_unlockable, a.affinity,
                                                second_related_affinity, third_related_affinity), standard_aff_three))

            # Find constellations for each set of possibility.
            first_rare_selection = list(map(lambda a: a.update_selected(a.affinity), rare_aff_one))
            print('FIRST RARE', first_rare_selection)
            first_rare_selection = [x for x in first_rare_selection if x]
            second_rare_selection = list(map(lambda a: a.update_selected(a.affinity), rare_aff_two))
            second_rare_selection = [x for x in second_rare_selection if x]
            third_rare_selection = list(map(lambda a: a.update_selected(a.affinity), rare_aff_three))
            third_rare_selection = [x for x in third_rare_selection if x]
            first_standard_selection = list(map(lambda a: a.update_selected(a.affinity), standard_aff_one))
            first_standard_selection = [x for x in first_standard_selection if x]
            second_standard_selection = list(map(lambda a: a.update_selected(a.affinity), standard_aff_two))
            second_standard_selection = [x for x in second_standard_selection if x]
            third_standard_selection = list(map(lambda a: a.update_selected(a.affinity), standard_aff_three))
            third_standard_selection = [x for x in third_standard_selection if x]
            # Let's calculate how many devotion points are needed to unlock a given list of constellations.
            add_up_members(first_rare_selection)
            add_up_members(second_rare_selection)
            add_up_members(third_rare_selection)
            add_up_members(first_standard_selection)
            add_up_members(second_standard_selection)
            add_up_members(third_standard_selection)
            # Pick a list of constellations with the lowest number of devotion points required.
            first_standard_pick = min(first_standard_selection, key=lambda a: a[-1])
            second_standard_pick = min(second_standard_selection, key=lambda a: a[-1])
            third_standard_pick = min(third_standard_selection, key=lambda a: a[-1])
            rare_pick_aff_one = min(first_rare_selection, key=lambda a: a[-1])
            rare_pick_aff_two = min(second_rare_selection, key=lambda a: a[-1])
            rare_pick_aff_three = min(third_rare_selection, key=lambda a: a[-1])
            # Create a FastMode object. It will facilitate the process of finding the fastest possible way to unlock a
            # desired star.
            rare_method = FastMode('rare method', rare_pick_aff_one, first_related_affinity,
                                   secondary=second_related_affinity, tertiary=third_related_affinity,
                                   poss_two=rare_pick_aff_two, poss_three=rare_pick_aff_three)
            rare_method.merge_possibilities()
            rare_first_result = [rare_method.calculate_devpoints(3), rare_method.merged]
            standard_method = FastMode('standard method', first_standard_pick, first_related_affinity,
                                       poss_two=second_standard_pick,
                                       secondary=second_related_affinity, tertiary=third_standard_pick,
                                       poss_three=third_standard_pick)
            standard_method.merge_possibilities()
            # Create a default mixed method object.
            mixed_method = FastMode(star.name, 0, first_related_affinity, secondary=second_related_affinity)
            first_rare_included = rare_method.evaluate_secondary_points(rare_method.secondary, rare_method.poss_one)
            second_rare_included = rare_method.evaluate_secondary_points(rare_method.tertiary, rare_method.poss_one)
            third_rare_included = rare_method.evaluate_secondary_points(rare_method.tertiary, rare_method.poss_two)
            # Find all possible constellations sets to unlock based on rare_included number.
            first_rare_contribution = stars_constellation.see_missing_points(requir=second_related_affinity)[
                                    second_related_affinity] - first_rare_included
            first_rare_match_possibilities = find_possibilities(second_related_affinity, after_rare=True,
                                                                rare=first_rare_included,
                                                                rare_contribution=first_rare_contribution)
            second_rare_ps = create_possibilities(first_rare_match_possibilities, second_related_affinity,
                                                  second_related_affinity)

            second_rare_contribution = stars_constellation.see_missing_points(
                requir=third_related_affinity)[third_related_affinity] - second_rare_included
            second_rare_match_possibilities = find_possibilities(third_related_affinity, after_rare=True,
                                                                 rare=second_rare_included,
                                                                 rare_contribution=second_rare_contribution)
            third_rare_ps = create_possibilities(second_rare_match_possibilities, third_related_affinity,
                                                 second_related_affinity)

            third_rare_contribution = \
                stars_constellation.see_missing_points(requir=third_related_affinity)[
                    third_related_affinity] - third_rare_included
            third_rare_match_possibilities = find_possibilities(third_related_affinity, after_rare=True,
                                                                rare=third_rare_included,
                                                                rare_contribution=third_rare_contribution)
            fourth_rare_ps = create_possibilities(third_rare_match_possibilities, third_related_affinity,
                                                  second_related_affinity)

            second_rare_selection = list(map(lambda a: a.update_options(const_affinity_bonus_unlockable,
                                             second_related_affinity, second_related_affinity,
                                             third_related_affinity), second_rare_ps))
            second_rare_selection = list(map(lambda a: a.update_selected(second_related_affinity), second_rare_ps))
            second_rare_selection = [x for x in second_rare_selection if x]
            third_rare_selection = list(map(lambda a: a.update_options(const_affinity_bonus_unlockable,
                                            third_related_affinity, second_related_affinity,
                                            third_related_affinity), third_rare_ps))
            third_rare_selection = list(map(lambda a: a.update_selected(third_related_affinity), third_rare_ps))
            third_rare_selection = [x for x in third_rare_selection if x]
            fourth_rare_selection = list(map(lambda a: a.update_options(const_affinity_bonus_unlockable,
                                             third_related_affinity, second_related_affinity, third_related_affinity),
                                             fourth_rare_ps))
            fourth_rare_selection = list(map(lambda a: a.update_selected(third_related_affinity), fourth_rare_ps))
            fourth_rare_selection = [x for x in third_rare_selection if x]
            add_up_members(second_rare_selection)
            add_up_members(third_rare_selection)
            rare_pick_aff_two = min(second_rare_selection, key=lambda a: a[-1])

            rare_pick_aff_three = min(third_rare_selection, key=lambda a: a[-1])
            rare_pick_aff_four = min(fourth_rare_selection, key=lambda a: a[-1])
            rare_method_vtwo = FastMode('rare version two', rare_pick_aff_one, first_related_affinity,
                                        secondary=second_related_affinity,
                                        tertiary=third_related_affinity,  poss_two=rare_pick_aff_two,
                                        poss_three=third_standard_pick)
            rare_method_vtwo.merge_possibilities()

            rare_method_vthree = FastMode('rare version three', rare_pick_aff_one, first_related_affinity,
                                          secondary=second_related_affinity,
                                          tertiary=third_related_affinity, poss_two=rare_pick_aff_two,
                                          poss_three=rare_pick_aff_four)
            rare_method_vthree.merge_possibilities()

            final_result = choose_best([standard_method, rare_method, rare_method_vthree, rare_method_vtwo], 3,
                                       standard_method, rare=rare_method, mixed=mixed_method,
                                       rare_two=rare_method_vtwo, rare_three=rare_method_vthree)

        list(map(lambda a: a.update_unlock_status() if type(a) != int else None, final_result))
        for i in final_result:
            if type(i) != int:
                i.unlock_fast()
        stars_constellation.unlock_till_star(star)
        list(map(standard_mode_lock, crossroads_list))
        split_stars = [x.name.replace(' ', '') for x in unlocked_stars]
        const_affinity_bonus_unlockable.clear()
        const_affinity_bonus.clear()
        return split_stars


def to_square_one(x):
    """
    Reset requirements of a constellation.
    :param x: A constellation.
    :return: Confirmation of execution.
    """
    for i in x.requirement:
        if type(x.requirement[i]) == list:
            x.requirement[i] = x.requirement[i][0]
    return True


def count_result(values_tuple):
    """
    Sum up values from attributes_dict keys.
    :param values_tuple: A tuple of values.
    :return: Percentage value if a dict value was a float, int value otherwise.
    """
    result = 0
    # if there is a flat value bigger than 0 as well as a percentage value in a tuple.
    if values_tuple[1] and values_tuple[0]:
        result = values_tuple[1] + (values_tuple[1] * values_tuple[0])
    # if there is only a flat value bigger than 0 in a tuple.
    elif values_tuple[1] and values_tuple[0] == 0:
        result = result + values_tuple[1]
    # if there is only a percentage value bigger than 0 in a tuple.
    elif values_tuple[1] == 0 and values_tuple[0]:
        result = result + values_tuple[0]

    if type(result) == int:
        return result
    elif type(result) == float and result < 10:
        return "{:.0%}".format(result)
    else:
        return int(result)


def dispatch_process():
    """
    Send results(all attributes and bonuses from attributes_dict) to the frontend of the app.
    :return: A list with all gained bonuses.
    """
    to_display = {key: value for (key, value) in attributes_dict.items() if value}
    values = list(map(lambda a: update_bonus_pool(a), list(to_display.keys())))
    values_two = list(map(lambda a: count_result(a), values))
    another_list = []
    counts = len(values_two)
    while len(another_list) < counts:
        for i in to_display:
            for item in values_two:
                another_list.append(i + ': ' + str(item))
                break
            del (to_display[i])
            values_two.remove(values_two[values_two.index(item)])
            break
    another_list = [x for x in another_list if 'Meter' not in x]
    to_dispatch = [x.replace('_', ' ') for x in another_list]
    return to_dispatch


def glow_stars():
    """
    Create a list of stars which could be unlocked.
    :return: A list with stars which could be unlocked and should receive a glowing effect.
    """
    not_unlocked = [x for x in stars_list if x not in unlocked_stars]
    to_flatten = list(map(lambda a: a.check_requirement(only_info=True), not_unlocked))
    to_glow = [item for sublist in to_flatten for item in sublist]
    to_glow = list(set(to_glow))
    return to_glow

# print(fast_mode(shieff))
# print(fast_mode(vire_fist))
# print(Points_of_Primordial)
# print(fast_mode(heavens_spear))
# print(standard_mode(usoldiet))
# standard_mode_lock(cleansing_waters)
# print(standard_mode_lock(ulos))
# print(fast_mode(abominable_might))
# print(standard_mode_lock(abominable_might))
# print(standard_mode(abominable_might))



