import json
import urllib.request

def get_ec2_prices(region='us-east-1'):
    url = f'https://ec2.shop/?region={region}&output=json'
    
    print(f'Buscando preços de instâncias AWS EC2 para a região {region}...')
    
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'curl/7.68.0'}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            raw_data = response.read().decode('utf-8')
            data = json.loads(raw_data)
            
            ec2_prices = []
            prices_list = data.get('Prices', [])
            
            for item in prices_list:
                instance_type = item.get('InstanceType')
                memory = float(item.get('Memory').replace(' GiB', ''))
                cpus = item.get('VCPUS')
                price_per_hour = item.get('Cost')
                monthly_cost = item.get('MonthlyPrice')
                
                if instance_type and price_per_hour is not None:
                    try:
                        price_per_hour = float(price_per_hour)
                        if price_per_hour > 0:
                            ec2_prices.append({
                                'instance_type': instance_type,
                                'memory': memory,
                                'cpus': cpus,
                                'price_per_hour': price_per_hour,
                                'monthly_cost': monthly_cost
                            })
                    except (ValueError, TypeError):
                        continue

            return ec2_prices

    except Exception as e:
        print(f'Erro ao consultar a API: {e}')
        return []


def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f'\nDados exportados para o arquivo: {filename}')


region_target = 'us-east-1'
results = get_ec2_prices(region=region_target)

print(f'\n{'Instância':<15} | {'Memória':<11} | {'vCPU':<11} | {'USD/Hora':<10} | {'USD/Mês':<10}')
print('-' * 67)

for item in results[:25]:
    print(
        f'{item['instance_type']:<15} | '
        f'${item['memory']:<10.2f} | '
        f'${item['cpus']:<10.2f} | '
        f'${item['price_per_hour']:<9.4f} | '
        f'${item['monthly_cost']:<14.2f}'
    )

print(f'\nQuantidade total de instâncias obtidas: {len(results)}')

output_filename = f'ec2_prices_{region_target}.json'
save_to_json(results, output_filename)