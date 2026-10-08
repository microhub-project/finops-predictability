import json, datetime
import pandas as pd

def filter_days(original_file, final_file):
    df = pd.read_csv(original_file, delimiter=';')

    new_df = df[df['infra_multiplier'] > 1.29]

    new_df.to_csv(final_file, sep=';', index=False)
    
def group_months():
    df = pd.read_csv('yearly-data.csv', delimiter=';')

    monthly_summary = round((df.groupby('month', as_index=False)[
        'infra_multiplier'
    ].max()), 2)

    monthly_summary.to_csv('monthly-data.csv', sep=';', index=False)
    
def suggest_scale(cpu, ram, monthly_cost, infra_multiplier, scale_type):
    
    if (scale_type == 'vertical'):    
        needed_cpus = cpu * infra_multiplier
        needed_ram = ram * infra_multiplier
    elif (scale_type == 'horizontal'):
        needed_cpus = cpu * (infra_multiplier - 1)
        needed_ram = ram * (infra_multiplier - 1)
    
    with open(f'ec2_prices_us-east-1.json', 'r') as file:
        data = json.load(file)
        
    options = []
        
    for i in range(len(data)):
        if (data[i]['memory'] >= needed_ram and data[i]['cpus'] >= needed_cpus):
            option = {
                'instance_type': data[i]['instance_type'],
                'memory': data[i]['memory'],
                'cpus': data[i]['cpus'],
                'price_per_hour': data[i]['price_per_hour'],
                'monthly_cost': data[i]['monthly_cost']
            }
            
            options.append(option)
            
    sorted_options = sorted(options, key=lambda x: x['monthly_cost'])
    cheapest_option = sorted_options[0]
    cheapest_option_monthly_cost = cheapest_option['monthly_cost']
    
    if scale_type == 'vertical':
        final_cost = cheapest_option_monthly_cost
        monthly_cost_increase = final_cost - monthly_cost
    elif scale_type == 'horizontal':
        monthly_cost_increase = cheapest_option_monthly_cost
        final_cost = monthly_cost + monthly_cost_increase

    increase_percentage = (monthly_cost_increase * 100) / monthly_cost

    #print(f'Tipo de Escalabilidade: {scale_type}')
    #print(f'Instância selecionada: {cheapest_option}')
    #print(f'Antes o custo era de ${round(monthly_cost, 2)}, agora o custo total será de ${round(final_cost, 2)}. Representando um aumento de ${round(monthly_cost_increase, 2)} ({round(increase_percentage, 2)}%).')
    
    result = {
        'scale_type': scale_type,
        'original_cost': round(monthly_cost, 2),
        'final_cost': round(final_cost, 2),
        'cost_increase': round(monthly_cost_increase, 2),
        'increase_percentage': round(increase_percentage, 2),
        'new_instance': cheapest_option
    }
    
    return result
    
    # json_data = json.dumps(result, indent=2)
    
    #file_name = f'{scale_type}.json'

    #with open(file_name, 'w') as json_file:
    #    json_file.write(json_data)
    
suggest_scale(2, 4, 18.83, 1.84, 'vertical')
suggest_scale(2, 4, 18.83, 1.84, 'horizontal')

def predict_year(infra_multiplier):
    predictions = {}
    
    for i in range(12):
        vertical = suggest_scale(2, 4, 18.83, infra_multiplier[i], 'vertical')
        horizontal = suggest_scale(2, 4, 18.83, infra_multiplier[i], 'horizontal')
        
        predictions[f'{i + 1}'] = {
            'infra_multiplier': infra_multiplier[i],
            'vertical': vertical,
            'horizontal': horizontal,
        }
        
    year = datetime.datetime.now().strftime('%Y')
    file_name = f'predictions_{year}.json'
    
    json_data = json.dumps(predictions, indent=2)
    
    with open(file_name, 'w') as json_file:
        json_file.write(json_data)
        
predict_year([1.23, 1.45, 1.8, 1.47, 2.07, 1.9, 2.06, 1.67, 1.66, 1.77, 6.65, 2.57])