import json
import os
import psutil
from time import sleep

cycle = 1  # 모니터링 사이클

while True:
    sm_info = dict()  # 시스템 전체 정보 (컨테이너수, 메모리, CPU )
    sm = dict()  # 시스템 모니터링 저장

    with open("con_info.text", "r", encoding="utf-8") as f:
        jason_text = f.readline()
        jason_text_object = json.loads(jason_text)

        # 시스템 전체정보 기록
        sm_info['sm_info'] = {'Number of containers running': len(
            jason_text_object), "All_CPU": psutil.cpu_count()*100, 'Memory': (psutil.virtual_memory().total)/1024**2}
        with open("data.json", "a") as s:
            json.dump(sm_info, s, indent='\t')
        sm_info.clear()

        print("Number of containers running: ", len(jason_text_object))
        print("All_CPU: ", str(psutil.cpu_count()*100)+"%")
        print("Memory: ", (psutil.virtual_memory().total)/1024**2, "MB")

        number = 0  # 컨테이너 번호

    # 기본자원,정적자원,동적자원 출력 코드
    for i in jason_text_object:
        f = os.popen(
            'curl -s --unix-socket /var/run/docker.sock http://localhost/containers/{}/stats?stream=false'.format(i.get('Id')))
        con_json = f.read()
        con_json = json.loads(con_json)

        cpu_delta = (con_json.get('cpu_stats').get('cpu_usage').get(
            'total_usage')) - (con_json.get('precpu_stats').get('cpu_usage').get('total_usage'))
        system_cpu_delta = (con_json.get('cpu_stats').get(
            'system_cpu_usage')) - (con_json.get('precpu_stats').get('system_cpu_usage'))
        number_cpus = con_json.get('cpu_stats').get('online_cpus')
        # 최종: cpu 사용량 계산
        cpu_use = (cpu_delta / system_cpu_delta)*number_cpus*100.0

        # 점유메모리
        used_memory = con_json.get('memory_stats').get(
            'usage')-con_json.get('memory_stats').get('stats').get('cache')  # jumyooyul

        # 메모리사용량
        available_memory = con_json.get('memory_stats').get('limit')
        memory_usage = (used_memory/available_memory)*100

        # 네트워크 체크
        tx_bytes = 0
        tx_packets = 0
        rx_bytes = 0
        rx_packets = 0

        tx_bytes += con_json.get('networks').get('eth0').get('tx_bytes')
        tx_packets += con_json.get('networks').get('eth0').get('tx_packets')
        rx_bytes += con_json.get('networks').get('eth0').get('rx_bytes')
        rx_packets += con_json.get('networks').get('eth0').get('rx_packets')

        sm['Container'+str(number)] = {'static_resource': {'PID': i.get('Id'), 'IPAdress': i.get(
            'NetworkSettings').get('Networks').get('bridge').get('IPAddress'), 'Macaddr': i.get(
            'NetworkSettings').get('Networks').get('bridge').get('MacAddress'), 'online_cpus': con_json.get(
            'precpu_stats').get('online_cpus'), 'memory_stats': con_json.get(
            'memory_stats').get('usage')},
            'dynamic_resource': {'cpu_use': cpu_use, 'used_memory': used_memory, 'memory_usage': memory_usage, 'tx_bytes': tx_bytes, 'tx_packets': tx_packets, 'rx_bytes': rx_bytes, 'rx_packets': rx_packets}}

        with open("data.json", "a") as s:
            json.dump(sm, s, indent='\t')
        sm.clear()  # 하나의 컨테이너 정보만 이어서 저장하도록 비워줘야한다

        print('\n-----------'+"Process ID: "+i.get('Id')+'-----------')
        print("NAMES: "+str(i.get('Names'))[3:-2])
        print(
            "IPAdress: "+i.get('NetworkSettings').get('Networks').get('bridge').get('IPAddress'))
        print(
            "Macaddr: "+i.get('NetworkSettings').get('Networks').get('bridge').get('MacAddress'))

        # cpu 개수
        print("online_cpus: " +
              str(con_json.get('precpu_stats').get('online_cpus')))
        # 전체 메모리사이즈
        memory_size = con_json.get('memory_stats').get('usage')
        print("memory-size:", memory_size)

        print("----------------dynamic-resource----------------")

        print("cpu-use: ", cpu_use)

        print("memory-use:", used_memory)

        print("memory_usage", memory_usage)

        print("tx_bytes: "+str(tx_bytes)+"(packets: "+str(tx_packets)+"), " +
              "rx_bytes: "+str(rx_bytes)+"(packet: "+str(rx_packets)+")")
        print("Memory-remaining: ", round(psutil.virtual_memory().total /
                                          1024**2-memory_size/1024**2, 2), "MB")
        print("The rest of cpu_percent: ",
              100-psutil.cpu_percent(), "%")

        print('----------')
        print("\n")

        number += 1  # json로그저장 container 수 체크 변수 +1
    print('---------------------------' +
          str(cycle)+' Monitoring---------------------------')
    cycle += 1
    sleep(2)
