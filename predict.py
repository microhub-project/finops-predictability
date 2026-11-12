import json, datetime
    
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
    
    #json_data = json.dumps(result, indent=2)
    
    return result
    
    #file_name = f'{scale_type}.json'

    #with open(file_name, 'w') as json_file:
    #    json_file.write(json_data)

def predict_year(mac, cpu, ram, monthly_cost, infra_multiplier):
    predictions = []
    
    for i in range(12):
        vertical = suggest_scale(cpu, ram, monthly_cost, infra_multiplier[i], 'vertical')
        horizontal = suggest_scale(cpu, ram, monthly_cost, infra_multiplier[i], 'horizontal')
    
        predictions.append({
            'month': i + 1,
            'infra_multiplier': infra_multiplier[i],
            'vertical': vertical,
            'horizontal': horizontal
        })
        
    #year = datetime.datetime.now().strftime('%Y')
    #file_name = f'{mac}_predictions_{year}.json'
    
    #json_data = json.dumps(predictions, indent=2)
    
    return {
        'mac_address': mac,
        'predictions': predictions
    }
    
    #with open(file_name, 'w') as json_file:
    #    json_file.write(json_data)
    
def predict_infra(instances, infra_multiplier):
    predictions = []
    
    for instance in instances:
        vertical = suggest_scale(instance.cpu, instance.ram, instance.monthly_cost, infra_multiplier, "vertical")
        horizontal = suggest_scale(instance.cpu, instance.ram, instance.monthly_cost, infra_multiplier, "horizontal")
        
        predictions.append({
            'mac': instance.mac,
            'vertical': vertical,
            'horizontal': horizontal
        })
    
    return predictions
    
def predict_year_infra(instances, infra_multiplier):
    predictions = []
    
    for instance in instances:
        prediction = predict_year(instance.mac, instance.cpu, instance.ram, instance.monthly_cost, infra_multiplier)
        
        predictions.append(
            prediction
        )
    
    return predictions

# https://economia.uol.com.br/noticias/redacao/2026/10/02/datas-duplas-ganham-forca-e-turbinam-vendas-de-grandes-marketplaces.htm
# https://www.ecommercebrasil.com.br/noticias/vendas-online-crescem-quase-40-na-semana-do-consumidor-aponta-levantamento-da-nuvemshop
# https://www.infomoney.com.br/consumo/vendas-em-e-commerce-e-varejo-aumentam-18-durante-semana-do-consumidor-diz-pesquisa/
# https://www.ecommercebrasil.com.br/noticias/vendas-aumentam-139-na-semana-do-cliente
# https://bis2bis.com.br/blog/datas-comemorativas-do-e-commerce/
# https://mundodomarketing.com.br/e-commerce-avanca-24-37-no-1-semestre-e-mira-r-260-bilhoes-em-2026