import tkinter as tk
import os
from tkinter import font

from datetime import datetime, timedelta
import json
from tkinter import *


dc_label=[]
dc_del_buttons=[]
dc_open=False

recipe_temp= {}
recipe= ''
checkbutton=None
recipename=''

# Pfad zu JSON-Dateien
file_path = os.path.join(os.path.dirname(__file__), 'food_data.json')
file_path_2 = os.path.join(os.path.dirname(__file__), 'recipes.json')
file_path_3 = os.path.join(os.path.dirname(__file__), 'history.json')
file_path_4 = os.path.join(os.path.dirname(__file__), 'settings.json')

try:
    with open(file_path) as file:
        food = json.load(file)
        print('die JSON Datei food_data.json wurde geladen')
except FileNotFoundError:
        food = {}

try:
    with open(file_path_2) as file2:
            recipes = json.load(file2)
            print('die JSON Datei recipes.json wurde geladen')
except FileNotFoundError:
        recipes = {}

try:
    with open(file_path_3) as file3:
            history = json.load(file3)
            print('die JSON Datei history.json wurde geladen')
except FileNotFoundError:
        history = {}

try:
    with open(file_path_4) as file4:
            settings = json.load(file4)
            print('die JSON Datei settings.json wurde geladen')
except FileNotFoundError:
        settings = {"goal":3500}

hundred_percent= settings["goal"]

def new_recipe(root):
    global food
    recipe_listbox.grid_remove()
    snack_listbox.grid_remove()  
    def entity_check(ingredient_to_test):
        global recipe_temp

        try:
            wert = food[ingredient_to_test][1]
            
        except:
            wert=recipe_temp[ingredient_to_test][1]
        if wert == 'entity':
            return True
        else: 
            return False
        
    def search(event=None):
        
        global food
        listbox.delete(0, tk.END)
        for k in food.keys():
            if ingredient.get().lower() in k:
                listbox.insert(tk.END, k)
        setup_ingredient()

    def click_suggested(event=None):
        select_index=listbox.curselection()
        if select_index:
            select_item = listbox.get(select_index)
            ingredient.delete(0, 100)
            ingredient.insert(0, select_item)
            listbox.delete(0, 100)
            amount.focus()
            setup_ingredient()

    def setup_ingredient(event=None):   
        ing=ingredient.get()
        
        if ing in food.keys():
            checkbutton.grid_remove()
                 
            if food[ing][1]== 'entity':
                entity.set(True)
                amount_label.config(text='amount[entitys]')
                ingredient_is.config(text='Entity',fg='orange')
            else:
                entity.set(False)
                amount_label.config(text='amount[g]')
                ingredient_is.config(text='Scalable', fg='green')
        else:
            checkbutton.grid()
            ingredient_is.config(text='')
            
            if entity.get() == True:
                amount_label.config(text='amount[entity]')
            else:
                amount_label.config(text='amount[g]')

    def ingredient_abschicken():                                        #start
        global recipe
        submitted_i=str(ingredient.get())
        submitted_a=amount.get()
        is_entity= entity.get()
        
    
        try: 

            if submitted_i != '' and ((submitted_a is not '' and submitted_a.isdecimal()) or is_entity==True):
                
                
                if is_entity==False:                                                        #Skalierbare Zutaten 
                    recipe_temp[submitted_i.lower()]=[float(submitted_a),'no_entity']
                    line = submitted_i[0:26].ljust(27, '.') + submitted_a.rjust(4)+ 'g'
                    
                elif submitted_a and is_entity==True:                                                           
                    recipe_temp[submitted_i.lower()]=[float(submitted_a),'entity']
                    line = submitted_i[0:26].ljust(27, '.') + submitted_a.rjust(4)+ 'x'
                    entity.set(False)
                
                else:
                    recipe_temp[submitted_i.lower()]=[float(1),'entity']
                    line = submitted_i[0:26].ljust(27, '.') + '1x'.rjust(5)
                    entity.set(False)

                recipe += line + '\n'
                
                last_ingredient = ingredient.get()
                ingredient.delete(0, tk.END)
                amount.delete(0, tk.END)
                             
                update_window(last_ingredient)
        except:
            print('amount is supposed to be an integer or float')
        
        setup_ingredient()
     
    def update_window(last_ingredient):
        
        description.config(text= 'Ingredient "' + str(last_ingredient) + '" was submitted. Enter another ingredient')
        recipe_label.config(text= 32* '_' + '\nRECIPE\n'+ 32*'-'+ '\n'+ recipe + 32*'_')
        ingredient.focus()

        
    def save():
        ingredient_abschicken()
        ingredient.destroy()
        ingredient_is.destroy()
        ingredient_label.destroy()
        amount.destroy()
        amount_label.destroy()
        listbox.destroy()
        listbox_label.destroy()
        submit.destroy()
        enter_recipe.destroy()
        checkbutton.grid_remove()

        check_dataavailability()

    def check_dataavailability():
        global food 
        new_ingredients =[]

        for i in recipe_temp.keys():
            if i in food.keys():
                continue
            else:
                new_ingredients.append(i)

                    
        def save_kcal():
            global food
            kcal_value= kcal_entry.get()
            
            
            if kcal_value:
                if entity_check(new_ingredients[0])==False:
                    food[str(new_ingredients[0].lower())]= [float(kcal_value),'no_entity']
                else:
                    food[str(new_ingredients[0].lower())]= [float(kcal_value),'entity',float(weight_entry.get())]

                print(new_ingredients[0]+ ' is saved')
                    
                kcal_entry.delete(0, tk.END)
                
                del new_ingredients[0]
                with open(file_path, 'w') as file:
                    json.dump(food, file)

                if new_ingredients:
                    description.config(text='Calorievalues of '+ str(len(new_ingredients)) + ' Ingredients are not saved in our data \n Enter value(s) for '+ str(new_ingredients[0]))
                    if entity_check(new_ingredients[0])==False:
                        kcal_label.config(text= 'calories per 100g'+ str(new_ingredients[0]))
                        weight_entry.grid_remove()
                        weight_label.grid_remove()
                    else:
                        kcal_label.config(text= 'calories of entity "' + str(new_ingredients[0])+ '"')
                       
                        weight_entry.grid()
                        weight_label.grid()
                       
                else:
                    description.config(text='All Ingredients are saved in our data')
                    kcal_entry.destroy()
                    kcal_submit.destroy()
                    kcal_label.destroy()
                    weight_entry.destroy()
                    weight_label.destroy()
                    recipe_calculation()

        
        
        if new_ingredients:
            description.config(text='Calorievalues of '+ str(len(new_ingredients)) + ' Ingredients are not saved in our data \n Enter values for '+ str(new_ingredients[0]))
            kcal_entry = tk.Entry(rezeptfenster)
            kcal_entry.grid(row=3, column= 1)
            kcal_entry.bind("<Return>", lambda event: save_kcal())
            kcal_entry.focus()
            kcal_submit = tk.Button(rezeptfenster, text= 'submit', command =save_kcal)
            kcal_submit.grid(row=5, column=1)
            weight_entry = tk.Entry(rezeptfenster)
            weight_entry.grid(row=4, column=1)
            weight_label= tk.Label(rezeptfenster, text= 'weight of entity')
            weight_label.grid(row=4, column=0)
            
            
            if entity_check(new_ingredients[0])==False:
                kcal_label = tk.Label(rezeptfenster, text= 'calories per 100g')
                kcal_label.grid(row=3, column =0) 
                weight_entry.grid_remove()
                weight_label.grid_remove()
                
            else:
                kcal_label = tk.Label(rezeptfenster, text= 'calories of entity ' +str(new_ingredients[0]))
                kcal_label.grid(row=3, column =0) 
                
        else:
            description.config(text='All Ingredients are saved in our data')
                    
            recipe_calculation()
                 
    def recipe_calculation():
        
        def recipe_save():
            global recipe, recipe_temp, recipename
            recipename= name.get().lower()
            if recipename is not '':
                try:
                    recipes[str(recipename)]= {"Calories":summe,"Weight": gewicht, "Calorie_density(per g)":calorie_density,"Ingredients":recipe_temp}
                        
                    with open(file_path_2, 'w') as recipefile:
                        json.dump(recipes, recipefile)
                        
                        print('Rezept gespeichert')

                        
                        on_close()
                except FileNotFoundError:
                    print('Rezept konnte nicht gespeichert werden. Fehler beim Laden der JSON Datei')

          

        summe=0
        gewicht=0
        for keys in recipe_temp.keys():
            if entity_check(keys)==False:
                summe += (recipe_temp[keys][0])*(food[keys][0])/100  
                gewicht += (recipe_temp[keys][0])
            else:
                summe += (food[keys][0]) * recipe_temp[keys][0]
                gewicht += (food[keys][2]) * recipe_temp[keys][0]
            
            print(summe)
                
       
        calorie_density= summe/gewicht 
        Antwort= '\n Your Recipe has '+ str(summe) +' Calories and weights ' +str(gewicht) +' gram in total. '
        actualize_json()
    
        description.config(text=Antwort)
        add.config(text='Safe Recipe and find it in your daily counter')

        name = tk.Entry(rezeptfenster)
        name.grid(row=6, column=0)
        name.bind("<Return>", lambda event: recipe_save())
        name.focus()
        
        name_submit =tk.Button(rezeptfenster, text='save', command= recipe_save)
        name_submit.grid(row=6, column=1)
        
        name_label= tk.Label(rezeptfenster, text='Choose a name for your recipe')
        name_label.grid(row=5, columnspan=2)

           

    #Fenster für Rezepterstellung
    rezeptfenster = tk.Toplevel(root)
    rezeptfenster.title('Recipe-Calculator')
    rezeptfenster.geometry('500x600')
    rezeptfenster.columnconfigure(0, weight=1)
    rezeptfenster.columnconfigure(1, weight=1)
    

    def on_close():
        global recipe_temp, recipe, recipename
        recipe_temp= {}
        recipe= ''
               
        
        if recipename!=0:
            Rezept.focus()
            recipe_entry.delete(0, tk.END)
            recipe_entry.insert(0, recipename)
            actualize_json()
            add_recipe()
            recipename=''
            recipe_listbox.new_json(recipes)
            
        rezeptfenster.destroy()
        
    rezeptfenster.protocol("WM_DELETE_WINDOW", on_close)
    
    description = tk.Label(rezeptfenster, text= 'We will calculate your meals calories. Enter your first ingredient \n ')
    description.grid(row=0, columnspan=3)

    ingredient_label= tk.Label(rezeptfenster, text= 'Enter a new Ingredient')
    ingredient_label.grid(row=1, column=0, sticky=E)

    input_var=tk.StringVar()
    input_var.trace_add("write", setup_ingredient)

    ingredient = tk.Entry(rezeptfenster, textvariable=input_var)
    ingredient.grid(row=1, column=1, sticky=W,padx=9)
    ingredient.focus()
    ingredient.bind("<Return>", lambda event: amount.focus()) 
    ingredient.bind("<KeyRelease>", search) 

    entity=tk.BooleanVar()
    checkbutton=Checkbutton(rezeptfenster, text="Add Ingredient as an entity", variable=entity, command=setup_ingredient)
    checkbutton.grid(row=5, column=1, sticky=W)


    ingredient_is=tk.Label(rezeptfenster, text='')
    ingredient_is.grid(row=5, column=1, sticky=W, padx=9)

    listbox = tk.Listbox(rezeptfenster)
    listbox.grid(row=2, column=1, sticky=W, padx=9)
    listbox.bind("<Double-Button-1>", click_suggested)

    listbox_label = tk.Label(rezeptfenster, text= 'or choose and doubleclick \n proposed Ingredients')
    listbox_label.grid(row=2, column=0, sticky=E)

    add = tk.Label(rezeptfenster, text= '')
    add.grid(row=2, columnspan=2)

    amount_label= tk.Label(rezeptfenster, text= 'amount[g]')
    amount_label.grid(row=4, column=0, sticky=E)
    
    amount= tk.Entry(rezeptfenster)
    amount.grid(row=4, column=1, sticky=W, padx=9)
    amount.bind("<Return>", lambda event: ingredient_abschicken()) 

    recipe_label= tk.Label(rezeptfenster, text= '\n ', font=("Courier", 12))
    recipe_label.grid(row=8, columnspan=2, sticky= EW)


    submit= tk.Button(rezeptfenster, text="submit ingredient", command= ingredient_abschicken)
    submit.grid(row=6,column=1, sticky=W, padx=9)

    enter_recipe= tk.Button(rezeptfenster, text="save recipe", command= save)
    enter_recipe.grid(row=9, column=1, sticky=W, padx=9)

    


def actualize_json():
    global food, recipes, daily_counter, history, settings
    date= str(datetime.now())[0:10]
    history[date]=daily_counter

    with open(file_path, 'w') as file:
        json.dump(food, file)
    with open(file_path_2, 'w') as file2:
        json.dump(recipes, file2)
    with open(file_path_3, 'w') as file3:
        json.dump(history, file3)
    with open(file_path_4, 'w') as file4:
        json.dump(settings, file4)
    try:
        with open(file_path) as file:
            food = json.load(file)
            print('die JSON Datei food_data.json wurde geladen')
    except FileNotFoundError:
        food = {}

    try:
        with open(file_path_2) as file2:
            recipes = json.load(file2)
            print('die JSON Datei recipes.json wurde geladen')
    except FileNotFoundError:
        recipes = {}
    
    try:
        with open(file_path_3) as file3:
            history = json.load(file3)
            print('die JSON Datei history.json wurde geladen')
    except FileNotFoundError:
        history = {}

    try:
        with open(file_path_4) as file4:
            settings = json.load(file4)
            print('die JSON Datei settings.json wurde geladen')
    except FileNotFoundError:
        settings = {"goal":3500}
    

def transform_entry(string):
    return float(string.replace(',','.'))

def is_number(string):
    try:
        transform_entry(string)
        return True
    except:
        return False

def access_dailycounter():
    global daily_counter
    date= str(datetime.now())[0:10]
    if date in history.keys():
        daily_counter=history[date]   
    else:
        daily_counter={}


def pie_adapt():
    access_dailycounter()                #Funktion zum plotten und aktualisieren des Kreisdiagramms
    pie_chart.delete("all")
    eaten_calories= sum(daily_counter.values())
    extent= (eaten_calories/hundred_percent) *360
    prozent= round((eaten_calories/hundred_percent) *100,2)
    pie_chart.create_arc(10, 10, 190, 190, start=0, extent= extent, fill= 'black', outline= 'white')
    pie_chart.create_arc(10, 10, 190, 190, start=extent, extent= 360-extent, fill= 'grey')
    pie_chart.create_oval(22,22,178,178, fill="lightgrey")
    pie_chart.create_text(105,100, text= str(prozent)+ '%', font=bold_font)
    label_counter.config(text="Daily Counter | " + str(round(eaten_calories))+'/'+str(hundred_percent))

    if dc_open ==True:
        display()

class PlaceholderEntry(tk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey'):
        super().__init__(master)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()

    def set_placeholder(self, new_placeholder):
        self.placeholder = new_placeholder
        self.delete(0, 'end')
        self.put_placeholder()


class vanishing_listbox(tk.Listbox):
    def __init__(self, master=None, entry= None, json_file= None, height=8, **kwargs):
        super().__init__(master, height=height, **kwargs)

        self.entry=entry
        self.json_file=json_file

        self.bind("<KeyRelease>", self.update_listbox)
        self.entry.bind("<KeyRelease>", self.update_listbox)
        self.bind("<Double-Button-1>", self.click_suggested)

    def new_json(self, json_file):
        self.json_file=json_file
    def update_listbox(self, *args):
        searchterm=self.entry.get().lower()
        self.delete(0, tk.END)
        if searchterm:
            
            for k in self.json_file.keys():
                if searchterm in k.lower():
                    self.insert(tk.END, k)

            if self.size() > 0:
                self.grid()
        
            else:
                self.grid_remove()
        else:
            self.grid_remove()

                
    def click_suggested(self, *args):
        select_index=self.curselection()
        if select_index:
            select_item = self.get(select_index)
            self.entry.delete(0, 100)
            self.entry.insert(0, select_item)
            self.delete(0, 100)
            self.grid_remove()
            self.entry.focus()
            self.entry.event_generate("<Return>")

#Funktionen zum Hinzufügen von Kalorienwerten zur Tagesbilanz
def add_estimate(*args):
    if recipe_entry.get() == recipe_entry.placeholder and snack_entry.get() == snack_entry.placeholder and is_number(estimate_entry.get())==True:
        Estimate_description = 'Estimate Value '
        e=2
        while Estimate_description in daily_counter.keys():
            new_description= "".join([i for i in Estimate_description if not i.isdigit()])
            Estimate_description = new_description+str(e)
            e+=1

        daily_counter[Estimate_description]=round(transform_entry(estimate_entry.get()),2)
        estimate_entry.delete(0, tk.END)
        print(daily_counter)
        actualize_json()
        pie_adapt()


def add_snack(*args):
    entry_items= snack_entry.get().lower()
    def close_new():
        new_label.destroy()
        button_save.destroy()
        button_x.destroy()
        amount_entry.destroy()
       
        try:
            new_kcal.destroy()
        except:
            None
        checkbutton_entity.grid_remove()
        checkbutton_scalable.grid_remove()
        snack_entry.config(state='normal')
        estimate_entry.config(state='normal')
        recipe_entry.config(state='normal')
        snack_entry.delete(0, tk.END)
        snack_entry.focus()
        Rezept.grid()

    def new(event=None):
        if entity_check.get()== False:
            new_ingredient()
        elif entity_check.get()==True:
            new_snack()

    def new_snack(event=None):
        if is_number(new_kcal.get())==True and is_number(amount_entry.get())==True:
            food[entry_items]= [transform_entry(new_kcal.get()),'entity', transform_entry(amount_entry.get())]
            daily_counter[entry_items+ ' 1.0x']= round(transform_entry(new_kcal.get()),2)
            
            actualize_json()
            snack_listbox.update_listbox()
            close_new()
            pie_adapt()
            print(daily_counter)


    def new_ingredient(event=None):
        if is_number(new_kcal.get())==True and is_number(amount_entry.get())==True:
            food[entry_items]= [transform_entry(new_kcal.get()),'no_entity']
            daily_counter[entry_items+ ' '+ str(amount_entry.get())+'g']= round((transform_entry(new_kcal.get()) *transform_entry(amount_entry.get()))/100.0,2)
            
            actualize_json()
            snack_listbox.update_listbox()
            close_new()
            pie_adapt()
            print(daily_counter)


    def enter_ingredient(event=None):                                                                           #function to add existing ingredient entitys and scalable ingredients...

        if is_number(amount_entry.get()):                                                                           #...in case user choose an amount for ingredient
            if food[entry_items][1]!='entity':                                                                             #and ingredient is an scalable one
                description=entry_items+ ' '+ str(transform_entry(amount_entry.get()))+'g'
                i=2
                while description in daily_counter.keys():
                    description += f" [{i}]"
                    i+=1

                daily_counter[description]=round((food[entry_items][0]*transform_entry(amount_entry.get()))/100.0,2)    
            else:                                                                                                           #and ingredient is an entity
                description=entry_items+ ' '+ str(transform_entry(amount_entry.get()))+'x'
                i=2
                while description in daily_counter.keys():
                    description += f" [{i}]"
                    i+=1
                daily_counter[description]=round(food[entry_items][0]*transform_entry(amount_entry.get()),2)
            close_new()
            actualize_json()
            pie_adapt()
            print(daily_counter)


        elif food[entry_items][1]=='entity':                                                                        #...in case user choose no amount for an entity ingredient, so default equals 1
            description=entry_items+ ' 1.0x'
            i=2
            while description in daily_counter.keys():
                description += f" [{i}]"
                i+=1
            daily_counter[description]=round(food[entry_items][0],2)
            close_new()
            actualize_json()
            pie_adapt()
            print(daily_counter)


    if recipe_entry.get() == recipe_entry.placeholder and estimate_entry.get() == estimate_entry.placeholder and snack_entry.get() != snack_entry.placeholder and snack_entry.get() != '':
        
        snack_entry.delete(0,tk.END)
        snack_entry.put_placeholder()
        snack_listbox.delete(0, tk.END)
        snack_listbox.grid_remove()
        estimate_entry.config(state='readonly')
        snack_entry.config(state='readonly')
        recipe_entry.config(state='readonly')
        new_label=tk.Label(root, text='Ingredient', font=small_bold_font)
        new_label.grid(row=1, column=5)
        button_x=tk.Button(root, text='x', bg='red', command=close_new)
        button_x.grid(row=0, column=5, sticky='e')

        button_save=tk.Button(root, text='save', command=new_snack)
        button_save.grid(row=5, column=5, sticky='e')
        
        Rezept.grid_remove()

        if entry_items in food.keys():
            button_save.config(command=enter_ingredient)
            
            if food[entry_items][1]!='entity':
                new_label.config(text='Scalable Ingredient\n'+ entry_items.upper())
                amount_entry=PlaceholderEntry(root, placeholder='amount[g]', color='green')
                amount_entry.grid(row=2, column=5)
                amount_entry.bind("<Return>", enter_ingredient)
            else:
                new_label.config(text='Ingredient Entity\n'+ entry_items.upper())
                amount_entry=PlaceholderEntry(root, placeholder='amount (default 1.0x) ', color='red')
                amount_entry.grid(row=2, column=5)
                amount_entry.bind("<Return>", enter_ingredient)
            
        else:
            checkbutton_entity.grid()
            checkbutton_scalable.grid()
            entity_check.set(False)
            new_label.config(text='New Ingredient\n'+entry_items.upper())
            new_kcal=PlaceholderEntry(root, placeholder='kcal/100g')
            new_kcal.grid(row=3,column=5)
            
            amount_entry=PlaceholderEntry(root, placeholder='amount[g]', color='green')
            amount_entry.grid(row=4, column=5)
            new_kcal.bind("<Return>", amount_entry.focus())
            amount_entry.bind("<Return>", new)

            def update_window():
                if entity_check.get()== False:
                    
                    new_kcal.set_placeholder('kcal/100g')
                    button_save.config(command=new_ingredient)
                    amount_entry.set_placeholder('amount[g]')
                    
                elif entity_check.get()==True: 

                    new_kcal.set_placeholder('kcal of Entity')
                    
                    amount_entry.set_placeholder('Weight[g] of Entity')
                    
                    button_save.config(command=new_snack)

            checkbutton_entity.config(command=update_window)
            checkbutton_scalable.config(command=update_window)
            update_window()
            

def add_recipe(event=None):
    
    def close_new():
        new_label.destroy()
        recipe_amount.destroy()
        button_g.destroy()
        button_percent.destroy()
        button_new_x.destroy()
        
        snack_entry.config(state='normal')
        estimate_entry.config(state='normal')
        recipe_entry.config(state='normal')
        recipe_entry.delete(0, tk.END)
        Rezept.grid()

    def close_new2():
        new_label.destroy()
        button_x.destroy()

        recipe_entry.delete(0, tk.END)

    def amount_g(event=None):
        amount= recipe_amount.get().replace('g','')
        if is_number(amount)==True:
            description= entry_scalable+' '+amount+ 'g'
            i=2
            while description in daily_counter.keys():
                description += f" [{i}]"
                i+=1
            daily_counter[description]= round(recipes[entry_scalable]['Calorie_density(per g)'] * transform_entry(amount),2)
            actualize_json()
            pie_adapt()
            close_new()
            print(daily_counter)

        
    def amount_percent(event=None):
        amount= recipe_amount.get().replace('%','')
        if is_number(amount)==True:
            description= entry_scalable+' '+amount+ '%'
            i=2
            while description in daily_counter.keys():
                description += f" [{i}]"
                i+=1
            daily_counter[description]= round(recipes[entry_scalable]['Calories'] * transform_entry(amount)/100.0,2)
            actualize_json()
            pie_adapt()
            close_new()
            print(daily_counter)


    entry_scalable= recipe_entry.get()
    if recipe_entry.get() != recipe_entry.placeholder and estimate_entry.get() == estimate_entry.placeholder and snack_entry.get() == snack_entry.placeholder and recipe_entry.get() != '':
        recipe_entry.delete(0, tk.END)
        recipe_entry.put_placeholder()
        Rezept.grid_remove()

        if entry_scalable in recipes.keys():
            new_label=tk.Label(root, text='Recipe \n'+ entry_scalable.upper(), font=small_bold_font)
            new_label.grid(row=1, column=5)
            
            snack_entry.config(state='readonly')
            estimate_entry.config(state='readonly')
            recipe_entry.config(state='readonly')

            recipe_amount=PlaceholderEntry(root, placeholder='amount')
            recipe_amount.grid(row=3,column=5)

            button_g=tk.Button(root, text='g', command=amount_g)
            button_g.grid(row=5, column=5, sticky='e')
           
            button_percent=tk.Button(root, text='%', command=amount_percent)
            button_percent.grid(row=5, column=5)
            
            button_new_x=tk.Button(root, text='x', bg='red', command=close_new)
            button_new_x.grid(row=0, column=5, sticky='e')

            recipe_amount.bind("<g>",amount_g)
            recipe_amount.bind("%", amount_percent)

    
        else:
            new_label=tk.Label(root, text= entry_scalable.upper()+'\n does not exist\n create a new recipe', font=small_bold_font)
            new_label.grid(row=1, column=5)
            button_x=tk.Button(root, text='x', bg='red', command=close_new2)
            button_x.grid(row=0, column=5, sticky='e')
            Rezept.grid()

def reset_dc(event=None):
    global daily_counter

    daily_counter = {}
    for label in dc_label:
            label.destroy()
    for button in dc_del_buttons:
            button.destroy() 
    dc_del_buttons.clear()
    dc_label.clear()
    actualize_json()
    pie_adapt()

def reset_daily_counter():
    global daily_counter
    date = str(datetime.now())[0:10]
    if date not in history:
        reset_dc()
    schedule_next_reset()

def display():                                                                                      #Funktion zu anzeigen der Einträge(daily counter)
    global dc_open
    root.geometry('580x600')
    dc_open=True
    
    def dc_close():
        global dc_open
        dc_open=False
        root.geometry('580x250')
        for label in dc_label:
            label.destroy()
        for button in dc_del_buttons:
            button.destroy() 
        dc_del_buttons.clear()
        dc_label.clear()
        close_entrylist.destroy()
        header.destroy()
        line.destroy()
        clear_dc_button.destroy()
               

    def delete(item):                                                                                   
        del daily_counter[item]
        print(daily_counter)
        for label in dc_label:
            label.destroy()
        for button in dc_del_buttons:
            button.destroy() 
        dc_del_buttons.clear()
        dc_label.clear()
        
        display()
        actualize_json()
        pie_adapt()


    line=tk.Label(root, text=55*'_',font=bold_courier)
    line.grid(row=6,column=1, columnspan=5, sticky=EW)
    header= tk.Label(root, text='Entry'+29*' '+'kcal\n'+ 38*'=',font=bold_courier)
    header.grid(row=7,column=1, columnspan=4, sticky= NE)

    close_entrylist= tk.Button(root, text='x', font=small_bold_font, bg='red', command=dc_close)
    close_entrylist.grid(row=7,column=5, sticky= E)
    
    
    row=8
    for k,v in daily_counter.items():
        label=tk.Label(root, text=k[0:30].ljust(31, '.') + str(v).rjust(7),font=("Courier", 12))
        label.grid(row=row, column=1, columnspan=4, sticky= E)
        dc_label.append(label)
        delete_button=tk.Button(root, text='x', fg='red', command=lambda item=k: delete(item))
        delete_button.grid(row=row, column=5, sticky=E)
        dc_del_buttons.append(delete_button)
        row+=1

    clear_dc_button=tk.Button(root, text='Clear Daily Counter', font=small_bold_font, bg='red', command=reset_dc)
    clear_dc_button.grid(row=2000, column=5, sticky=E)

def schedule_next_reset():
    now = datetime.now()
    next_midnight = datetime.combine(now + timedelta(days=1), datetime.min.time())
    delay = (next_midnight - now).total_seconds()
    root.after(int(delay * 1000), reset_daily_counter)  # Convert delay to milliseconds



# Erstellen eines Hauptfensters
root = tk.Tk()

root.title("Calorie-Tracker")
root.geometry('580x250')
#root.configure(bg='white')
bold_font = font.Font(family="Helvetica", size=18, weight="bold")
small_bold_font = font.Font(family="Helvetica", size=11 , weight="bold")
bold_courier = font.Font(family="Courier", size=12 , weight="bold")



# Erstellen des Kreisdiagramms
pie_chart=tk.Canvas(root, width=200, height=200, bg='lightgrey')
pie_chart.grid(rowspan=4, column=1)

# Erstellen eines Beschriftungselemente
label_counter = tk.Button(root, text="Daily Counter | 0/"+str(hundred_percent), font=small_bold_font, command=display)
label_counter.grid(row=5, column=1, sticky=EW)

line = tk.Canvas(root, width=10, height=200)
line.grid(row=0, rowspan=5, column=2)
line.create_line(6, 10, 6, 200, fill="black", width=2)

line2 = tk.Canvas(root, width=10, height=200)
line2.grid(row=0, rowspan=5, column=4)
line2.create_line(6, 10, 6, 200, fill="black", width=2)

enter= tk.Label(root, text='Enter or Search...', font=small_bold_font)
enter.grid(row=0, column=3)
estimate_entry=PlaceholderEntry(root, placeholder='...an estimate value', color='blue')
estimate_entry.grid(row=1, column=3)
estimate_entry.bind("<Return>", add_estimate)

snack_entry=PlaceholderEntry(root, placeholder='...ingredients', color='green')
snack_entry.grid(row=2, column=3)
snack_entry.bind("<Return>", add_snack)

snack_listbox=vanishing_listbox(root, entry=snack_entry, json_file=food)
snack_listbox.grid(row=1, rowspan=3, column=5)
snack_listbox.grid_remove()

recipe_entry=PlaceholderEntry(root, placeholder='...Recipes', color='brown')
recipe_entry.grid(row=3, column=3)
recipe_entry.bind("<Return>", add_recipe)

recipe_listbox=vanishing_listbox(root, entry=recipe_entry, json_file= recipes)
recipe_listbox.grid(row=1, rowspan=3, column=5)
recipe_listbox.grid_remove()



entity_check=tk.BooleanVar()
checkbutton_entity=Checkbutton(root, text="Entity",variable=entity_check, onvalue= True, offvalue=False)
checkbutton_entity.grid(row=2, column=5, sticky=W)

checkbutton_scalable=Checkbutton(root, text="Scalable", variable=entity_check, onvalue=False, offvalue=True)
checkbutton_scalable.grid(row=2, column=5, sticky=E)
checkbutton_entity.grid_remove()
checkbutton_scalable.grid_remove()

enter_button = tk.Button(root, text="Enter", font=small_bold_font, command=lambda: [add_estimate(), add_recipe(), add_snack()])               #alternativ text="\u21B5"
enter_button.grid(row=5, column=3, sticky='e')


Rezept = tk.Button(root, text="Create a new recipe", font=small_bold_font, command=lambda: new_recipe(root))
Rezept.grid(row=5, column=5, sticky='w')



pie_adapt()


schedule_next_reset()


# Hauptereignisschleife starten
root.mainloop()

