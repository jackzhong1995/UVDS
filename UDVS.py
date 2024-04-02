import sys
import gzip
import concurrent.futures

def process_vcf_file(input_file_path, output_file_path, num_workers=4):
    seen_coordinates = set()  # 创建一个空集合来存储已经出现过的坐标
    unique_vcf_entries = []   # 存储唯一的VCF条目

    with gzip.open(input_file_path, 'rt') as file:
        for line in file:
            if line.startswith('#'):  # 如果是注释行，直接记录到输出列表
                unique_vcf_entries.append(line)
            else:
                fields = line.strip().split('\t')
                coordinate = f"{fields[0]}:{fields[1]}"
                if coordinate not in seen_coordinates:  # 如果坐标不存在，记录到输出列表，并添加到seen_coordinates
                    seen_coordinates.add(coordinate)
                    unique_vcf_entries.append(line)

    with gzip.open(output_file_path, 'wt') as file:
        for entry in unique_vcf_entries:  # 写入所有唯一的记录到输出文件
            file.write(entry)

    print(f"Unique VCF entries have been written to {output_file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python rm.vcfdup.py input_vcf_file output_vcf_file num_workers")
        sys.exit(1)
    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]
    num_workers = int(sys.argv[3])
    process_vcf_file(input_file_path, output_file_path, num_workers)