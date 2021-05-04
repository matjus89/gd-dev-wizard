from flask import Flask, render_template, url_for, request, jsonify
from classes_and_functions import *


static_dir = ('/static')
app = Flask(__name__)


@app.route('/main/')
def title():
    return render_template("gd.html")


# Welcome page.
@app.route('/')
def welcome():
    return render_template('welcome2.html')

# The main functionality of the site, the blink mode that lets a user unlock even third tier star with one click.
@app.route('/main/blink_mode', methods=['GET', 'POST'])
def blink_mode():
    if request.method == 'POST':
        clickedItem = request.form.get("clickedItem")
        fast_mode(eval(clickedItem))
        for i in unlocked_stars:
            if 'skill' in i.name:
                i.name = i.name.replace('skill', '')
    return jsonify(result=[x.name.replace(' ', '') for x in unlocked_stars], asc=Points_of_Ascendant.points,
                   chs=Points_of_Chaos.points, eld=Points_of_Eldritch.points, ord=Points_of_Order.points,
                   prim=Points_of_Primordial.points, devpoints=Devotion_Points_Pool.devpoints,
                   to_glow=[x.name.replace(' ', '') for x in glow_stars()])


# Resets the whole application to its default state.
@app.route('/main/reset', methods=['GET', 'POST'])
def reset():
    if request.method == 'POST':
        for i in attributes_dict:
            attributes_dict[i].clear()
        list(map(lambda a: a.reset_unlock_status(), constellations))
        list(map(lambda a: a.requirs_reset(), constellations))
        unlocked_stars.clear()
        for i in constellations:
            i.update_unlock_status()
            if i.original is not None:
                i.reset_requirement()
        for i in affinities:
            i.zero()
            i.reset_minimum()
        Devotion_Points_Pool.reset()
    return jsonify(result=[x.name.replace(' ', '') for x in unlocked_stars], devpoints=Devotion_Points_Pool.devpoints,
                   asc=Points_of_Ascendant.points, chs=Points_of_Chaos.points, eld=Points_of_Eldritch.points,
                   ord=Points_of_Order.points, prim=Points_of_Primordial.points)


# Enables a user to unlock a star using the standard in-game mechanics.
@app.route('/main/standard', methods=['GET', 'POST'])
def standard():
    if request.method == 'POST':
        clickedItem = request.form['data']
        global instance_name
        instance_name = eval(clickedItem)
        standard_mode(instance_name)
        print(type(instance_name.name))
    return jsonify(result=instance_name in unlocked_stars, asc=Points_of_Ascendant.points, chs=Points_of_Chaos.points,
                   eld=Points_of_Eldritch.points, ord=Points_of_Order.points, prim=Points_of_Primordial.points,
                   devpoints=Devotion_Points_Pool.devpoints, to_glow=[x.name.replace(' ', '') for x in glow_stars()])


# Enables a user to lock a star using the standard in-game mechanics.
@app.route('/main/standard_lock', methods=['GET', 'POST'])
def standard_lock():
    if request.method == 'POST':
        clickedItem = request.form['data']
        global instance_name
        instance_name = eval(clickedItem)
        standard_mode_lock(instance_name)
        print(type(instance_name.name))
    return jsonify(result=instance_name in unlocked_stars, asc=Points_of_Ascendant.points, chs=Points_of_Chaos.points,
                   eld=Points_of_Eldritch.points, ord=Points_of_Order.points, prim=Points_of_Primordial.points,
                   devpoints=Devotion_Points_Pool.devpoints, to_glow=[x.name.replace(' ', '') for x in glow_stars()])


# Display attributes of any hovered star.
@app.route('/main/display_attributes', methods=['GET', 'POST'])
def display_attributes():
    second_bonus = None
    second_bonus_value = None
    second_affinity = None
    second_affinity_value = None
    third_affinity = None
    third_affinity_value = None
    if request.method == 'POST':
        hoveredItem = request.form['data']
        global instance_name
        instance_name = eval(hoveredItem)
        print(type(instance_name.name))
    const = instance_name.find_constellation()
    first_affinity = list(const.requirement.keys())[0]
    first_affinity_value = const.requirement[list(const.requirement.keys())[0]]
    if len(const.requirement) == 2:
        second_affinity = list(const.requirement.keys())[1]
        second_affinity_value = const.requirement[list(const.requirement.keys())[1]]
    if len(const.requirement) == 3:
        second_affinity = list(const.requirement.keys())[1]
        second_affinity_value = const.requirement[list(const.requirement.keys())[1]]
        third_affinity = list(const.requirement.keys())[2]
        third_affinity_value = const.requirement[list(const.requirement.keys())[2]]
    if type(const.affinity_bonus) == dict:
        first_bonus = list(const.affinity_bonus.keys())[0]
        first_bonus_value = const.affinity_bonus[list(const.affinity_bonus.keys())[0]]
    else:
        first_bonus = 'no affinity bonus'
        first_bonus_value = 0
    if len(const.affinity_bonus) == 2:
        second_bonus = list(const.affinity_bonus.keys())[1]
        second_bonus_value = const.affinity_bonus[list(const.affinity_bonus.keys())[1]]

    return jsonify(result=instance_name.display_attr(), first_affinity=first_affinity, second_affinity=second_affinity,
                   third_affinity=third_affinity, first_affinity_value=first_affinity_value,
                   second_affinity_value=second_affinity_value, third_affinity_value=third_affinity_value,
                   first_bonus=first_bonus, second_bonus=second_bonus,
                   first_bonus_value=first_bonus_value, second_bonus_value=second_bonus_value)


# Displays results that is all bonuses to attributes gained by unlocking stars.
@app.route('/main/display_results', methods=['GET', 'POST'])
def display_results():
    to_dispatch = dispatch_process()
    return jsonify(result=to_dispatch)


if __name__ == '__main__':
    app.run(debug=True)
