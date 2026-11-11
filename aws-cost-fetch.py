from dotenv import load_dotenv
import os, pymysql, json, urllib.request, uuid

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
                memory = round(float(item.get('Memory').replace(' GiB', '')), 2)
                cpus = item.get('VCPUS')
                price_per_hour = item.get('Cost')
                monthly_cost = round(item.get('MonthlyPrice'), 2)
                
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
print(f'Quantidade total de instâncias obtidas: {len(results)}')

# output_filename = f'ec2_prices_{region_target}.json'
# save_to_json(results, output_filename)

load_dotenv()

conexao = pymysql.connect(
    host=os.getenv("host"),
    user=os.getenv("user"),
    password=os.getenv("password"),
    database=os.getenv("database"),
)

cursor = conexao.cursor()

for item in results:
    instance_type = item['instance_type']
    cpus = item['cpus']
    memory = item['memory']
    monthly_cost = item['monthly_cost']
    
    cursor.execute(
        'SELECT nome, cpu, ram, custo_computacao FROM tipo WHERE nome = %s;',
        (instance_type,)
    )
    tipo = cursor.fetchone()
    
    if tipo is None:
        tipoUUID = str(uuid.uuid4())
        cursor.execute(
            'INSERT INTO tipo (uuid, nome, cpu, ram, custo_computacao) VALUES (UUID_TO_BIN(%s), %s, %s, %s, %s);',
            (tipoUUID, instance_type, cpus, memory, monthly_cost)
        )
        print(f'Tipo de instância {instance_type} inserido com sucesso: CPU = {cpus}, RAM = {memory}, CUSTO = R$ {monthly_cost}')
    else:
        if (
            tipo[1] != cpus
            or float(tipo[2]) != memory
            or float(tipo[3]) != monthly_cost
        ):
            cursor.execute(
                'UPDATE tipo SET cpu = %s, ram = %s, custo_computacao = %s, atualizado_em = CURRENT_TIMESTAMP() WHERE nome = %s;',
                (cpus, memory, monthly_cost, instance_type)
            )
            print(f'Tipo de instância {instance_type} atualizado com sucesso: CPU ({tipo[1]} -> {cpus}), RAM ({tipo[2]} -> {memory}), CUSTO (R$ {tipo[3]} -> R$ {monthly_cost})')

conexao.commit()

cursor.close()
conexao.close()