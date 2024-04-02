import sys
import gzip
import concurrent.futures

def process_vcf_file(input_file_path, output_file_path, num_workers=4):
    seen_coordinates = set()  # ����һ���ռ������洢�Ѿ����ֹ�������
    unique_vcf_entries = []   # �洢Ψһ��VCF��Ŀ

    with gzip.open(input_file_path, 'rt') as file:
        for line in file:
            if line.startswith('#'):  # �����ע���У�ֱ�Ӽ�¼������б�
                unique_vcf_entries.append(line)
            else:
                fields = line.strip().split('\t')
                coordinate = f"{fields[0]}:{fields[1]}"
                if coordinate not in seen_coordinates:  # ������겻���ڣ���¼������б�����ӵ�seen_coordinates
                    seen_coordinates.add(coordinate)
                    unique_vcf_entries.append(line)

    with gzip.open(output_file_path, 'wt') as file:
        for entry in unique_vcf_entries:  # д������Ψһ�ļ�¼������ļ�
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