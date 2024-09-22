from io import BytesIO 
import base64
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd

def get_graph():
   #create a BytesIO buffer for the image
   buffer = BytesIO()         

   #create a plot with a bytesIO object as a file-like object. Set format to png
   plt.savefig(buffer, format='png')

   #set cursor to the beginning of the stream
   buffer.seek(0)

   #retrieve the content of the file
   image_png=buffer.getvalue()

   #encode the bytes-like object
   graph=base64.b64encode(image_png)

   #decode to get the string as output
   graph=graph.decode('utf-8')

   #free up the memory of buffer
   buffer.close()

   #return the image/graph
   return graph

#chart_type: user input o type of chart,
#data: pandas dataframe
def get_chart(chart_type, qs):
    #switch plot backend to AGG (Anti-Grain Geometry) - to write to file
    #AGG is preferred solution to write PNG files
    plt.switch_backend('AGG')

    #specify figure size
    
    data = pd.DataFrame(qs)
    data = data.sort_values(by='name') 

    if chart_type == 'BC':
        fig=plt.figure(figsize=(6,4))

        # Define the bins and labels
        bins = [0, 5, 10, 30, 60, float('inf')]  # Inf represents anything above 60
        labels = [' < 5', '5 - 10', '10 - 30', '30 - 60', '60 <']
         
        # Create a new column 'cooking_time_category' with the binned values
        data['cooking_time_category'] = pd.cut(data['cooking_time'], bins=bins, labels=labels)
        cooking_time_counts = data['cooking_time_category'].value_counts(sort=False)  # Don't sort so the labels are in bin order

        plt.bar(cooking_time_counts.index, cooking_time_counts.values, color="#78C2AD", zorder=1)
        plt.gca().yaxis.set_major_locator(mtick.MaxNLocator(integer=True))
        plt.xlabel('Cooking Time Categories')
        plt.ylabel('Number of Recipes')
        plt.title('Bar Chart: Cooking Time Categories vs Number of Recipes')
        plt.grid(True, axis='y', color='lightgrey', linestyle='--', linewidth=0.5, zorder=0)

    elif chart_type == 'PC':
        colors = ['#78C2AD','#82CCDB','#FFD57E','#FF8C6B']
        fig=plt.figure(figsize=(6,4))
        difficulty_counts = data['difficulty'].value_counts()
        plt.pie(difficulty_counts, labels=difficulty_counts.index, colors=colors, wedgeprops={"linewidth": 0.75, "edgecolor": "white"}, autopct='%1.1f%%', startangle=180)
        plt.title('Pie Chart: Recipe Difficulty')
        

    elif chart_type == 'LC':   
        fig=plt.figure(figsize=(6,6)) 
        data['num_ingredients'] = data['ingredients'].apply(lambda x: len(x.split(',')))
        plt.plot(data['name'], data['num_ingredients'], color="#78C2AD", marker='o')
        plt.xlabel('Recipe Name')
        plt.ylabel('Number of Ingredients')
        plt.title('Line Chart: Recipe Name vs. Number of Ingredients')
        plt.xticks(rotation=45, ha='right', fontsize=8)
        plt.grid(True, color='lightgrey', linestyle='--', linewidth=0.5)

    else:
        print ('unknown chart type')

    #specify layout details
    plt.tight_layout()

    #render the graph to file
    chart = get_graph() 

    # to prevent memory leaks
    plt.close(fig)

    return chart       