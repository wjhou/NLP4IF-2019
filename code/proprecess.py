import os
import csv
import sys

def read_tsv(input_file, quotechar=None):
	with open(input_file, "r", encoding="utf-8") as f:
		reader = csv.reader(f, delimiter="\t", quotechar=quotechar)
		lines = []
		for line in reader:
			if sys.version_info[0] == 2:
				line = list(unicode(cell, 'utf-8') for cell in line)
			lines.append(line)
		return lines

def extract(source_text_folder, output_file, source_label_folder=None):
	text_files = os.listdir(source_text_folder)

	tsv_lines = []

	for text_file in text_files:
		lines = read_tsv(os.path.join(source_text_folder, text_file))
		article_id = text_file.split('.')[0]
		if source_label_folder is not None:
			slc_label_file = article_id + '.task-SLC.labels'
			slc_labels = read_tsv(os.path.join(source_label_folder+'-SLC', slc_label_file))
		else:
			slc_labels = [[article_id.replace('article', ''), str(i+1), 'non-propaganda'] for i in range(len(lines))]

		for line, slc_label in zip(lines, slc_labels):
			if len(line) == 0:
				line = ['[EMPTY]']
			tsv_line = '\t'.join(line+slc_label)
			tsv_lines.append(tsv_line)
	with open(output_file, 'w', encoding='utf-8') as f:
		for line in tsv_lines:
			f.write(line + '\n')


if __name__ == '__main__':
	if not os.path.exists('data'):
		os.mkdir('data')
	extract('datasets_v2/train-articles', 'data/train.tsv', 'datasets_v2/train-labels')
	extract('datasets_v2/dev-articles', 'data/dev.tsv')
	extract('datasets_v2/test-articles', 'data/test.tsv')