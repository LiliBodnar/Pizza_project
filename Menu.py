def display_menu(cursor): 
    # Fetch the menu items and their details from the database
    cursor.execute("SELECT ItemID, ItemName, ItemType FROM Item")
    items = cursor.fetchall()

    # Create a dictionary to hold the ingredients for each item
    ingredients_dict = {}
    prices_dict = {}
    cursor.execute("""
        SELECT il.ItemID, i.IngredientName, i.Price 
        FROM IngredientList il 
        JOIN Ingredient i ON il.IngredientID = i.IngredientID
    """)
    ingredient_list = cursor.fetchall()

    for item_id, ingredient_name, price in ingredient_list:
        if item_id not in ingredients_dict:
            ingredients_dict[item_id] = []
            prices_dict[item_id] = 0  # Initialize the price for the item
        ingredients_dict[item_id].append(ingredient_name)
        prices_dict[item_id] += price  # Sum the ingredient prices for each item

    # Fetch dietary restrictions for items
    restrictions_dict = {}
    cursor.execute("""
        SELECT il.ItemID, rt.Vegan, rt.Vegetarian, rt.GlutenFree, rt.LactoseFree 
        FROM IngredientList il
        JOIN IngredientType it ON il.IngredientID = it.IngredientID
        JOIN RestrictionType rt ON it.RestrictionTypeID = rt.RestrictionTypeID
    """)
    restrictions = cursor.fetchall()

    for item_id, vegan, vegetarian, gluten_free, lactose_free in restrictions:
        restrictions_dict[item_id] = {
            'Vegan': vegan,
            'Vegetarian': vegetarian,
            'GlutenFree': gluten_free,
            'LactoseFree': lactose_free
        }

    print("------------------Menu:------------------")
    print("")

    # Display Pizzas
    pizza_items = [item for item in items if item[2] == 'Pizza']
    if pizza_items:
        print("Pizzas:")
        for item in pizza_items:
            item_id = item[0]
            item_name = item[1]
            price = prices_dict.get(item_id, "N/A")  # Get the total price for the item
            restrictions = restrictions_dict.get(item_id, {})
            ingredients = ", ".join(ingredients_dict.get(item_id, []))
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
                print(f"- {item_name:<20} {restrictions_str:<20} €{price:.2f}")
            else:
                print(f"- {item_name:<20} {restrictions_str:<20} €{price}")
                
            print(f"  {ingredients}")  
            print("")

    # Display Drinks
    drink_items = [item for item in items if item[2] == 'Drink']
    if drink_items:
        print("\nDrinks:")
        for item in drink_items:
            item_id = item[0]
            item_name = item[1]
            price = prices_dict.get(item_id, "N/A")
            print(f"- {item_name:<40} €{price:.2f}")

    # Display Desserts
    dessert_items = [item for item in items if item[2] == 'Dessert']
    if dessert_items:
        print("\nDesserts:")
        for item in dessert_items:
            item_id = item[0]
            item_name = item[1]
            price = prices_dict.get(item_id, "N/A")
            restrictions = restrictions_dict.get(item_id, {})
            #ingredients = ", ".join(ingredients_dict.get(item_id, []))
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
            print(f"- {item_name:<20} {restrictions_str:<20} €{price:.2f}")
            #print(f"  {ingredients}")  # Print ingredients below

    print()  
