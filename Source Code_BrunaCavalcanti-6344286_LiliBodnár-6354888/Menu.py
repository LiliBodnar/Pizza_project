def display_menu(cursor):
    cursor.execute("SELECT ItemID, ItemName, ItemType FROM Item")
    items = cursor.fetchall()

    ingredients_dict = {}
    prices_dict = {}
    cursor.execute("""
        SELECT il.ItemID, i.IngredientID, i.IngredientName, i.Price 
        FROM IngredientList il 
        JOIN Ingredient i ON il.IngredientID = i.IngredientID
    """)
    ingredient_list = cursor.fetchall()

    for item_id, ingredient_id, ingredient_name, price in ingredient_list:
        if item_id not in ingredients_dict:
            ingredients_dict[item_id] = []
            prices_dict[item_id] = 0
        ingredients_dict[item_id].append(ingredient_name)
        prices_dict[item_id] += price 

    ingredient_restrictions = {}
    cursor.execute("""
        SELECT i.IngredientID, rt.Vegan, rt.Vegetarian, rt.GlutenFree, rt.LactoseFree
        FROM Ingredient i
        JOIN IngredientType it ON i.IngredientID = it.IngredientID
        JOIN RestrictionType rt ON it.RestrictionTypeID = rt.RestrictionTypeID
    """)
    restrictions = cursor.fetchall()

    for ingredient_id, vegan, vegetarian, gluten_free, lactose_free in restrictions:
        ingredient_restrictions[ingredient_id] = {
            'Vegan': bool(vegan),
            'Vegetarian': bool(vegetarian),
            'GlutenFree': bool(gluten_free),
            'LactoseFree': bool(lactose_free)
        }


    print("------------------Menu:------------------")
    print("")

    item_number = 1 

    def aggregate_restrictions(item_id):
        item_ingredients = [ingr for ingr in ingredient_list if ingr[0] == item_id]
        item_restrictions = {'Vegan': True, 'Vegetarian': True, 'GlutenFree': True, 'LactoseFree': True}

        if(item_id == 9):
            item_restrictions = {'Vegan': False, 'Vegetarian': False, 'GlutenFree': False, 'LactoseFree': False}
        else:
            for item_id, ingredient_id, ingredient_name, price in item_ingredients:
                ingr_restrictions = ingredient_restrictions.get(ingredient_id, {})
                
                item_restrictions['Vegan'] = item_restrictions['Vegan'] and ingr_restrictions.get('Vegan', True)
                item_restrictions['Vegetarian'] = item_restrictions['Vegetarian'] and ingr_restrictions.get('Vegetarian', True)
                item_restrictions['GlutenFree'] = item_restrictions['GlutenFree'] and ingr_restrictions.get('GlutenFree', True)
                item_restrictions['LactoseFree'] = item_restrictions['LactoseFree'] and ingr_restrictions.get('LactoseFree', True)
    
        return item_restrictions

    pizza_items = [item for item in items if item[2] == 'Pizza']
    if pizza_items:
        print("Pizzas:")
        for item in pizza_items:
            item_id = item[0]
            item_name = item[1]
            price = prices_dict.get(item_id, "N/A")  
            ingredients = ", ".join(ingredients_dict.get(item_id, []))
            
            restrictions = aggregate_restrictions(item_id)
            
            restrictions_list = []
            if restrictions.get('Vegan'):
                restrictions_list.append("VG")
            if restrictions.get('Vegetarian'):
                restrictions_list.append("V")
            if restrictions.get('GlutenFree'):
                restrictions_list.append("GF")
            if restrictions.get('LactoseFree'):
                restrictions_list.append("LF")

            restrictions_str = ", ".join(restrictions_list) if restrictions_list else " "
            if isinstance(price, (int, float)):
                print(f"{item_number}. {item_name:<20} {restrictions_str:<20} €{price:.2f}")
            else:
                print(f"{item_number}. {item_name:<20} {restrictions_str:<20} €{price}")

            print(f"   {ingredients}") 
            print("")
            item_number += 1 

    drink_items = [item for item in items if item[2] == 'Drink']
    if drink_items:
        print("\nDrinks:")
        for item in drink_items:
            item_id = item[0]
            item_name = item[1]
            price = prices_dict.get(item_id, "N/A")
            print(f"{item_number}. {item_name:<40} €{price:.2f}")
            item_number += 1 

    dessert_items = [item for item in items if item[2] == 'Dessert']
    if dessert_items:
        print("\nDesserts:")
        for item in dessert_items:
            item_id = item[0]
            item_name = item[1]
            price = prices_dict.get(item_id, "N/A")
            restrictions = aggregate_restrictions(item_id)
            restrictions_list = []
            if restrictions.get('Vegetarian'):
                restrictions_list.append("V")
            if restrictions.get('Vegan'):
                restrictions_list.append("VG")
            if restrictions.get('GlutenFree'):
                restrictions_list.append("GF")
            if restrictions.get('LactoseFree'):
                restrictions_list.append("LF")

            restrictions_str = ", ".join(restrictions_list) if restrictions_list else " "
            print(f"{item_number}. {item_name:<20} {restrictions_str:<20} €{price:.2f}")
            item_number += 1  

    print() 
