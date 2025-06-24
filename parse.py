import os
import csv
from bs4 import BeautifulSoup

def parse_file(file_path):
    verse_lines = []
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        
        # Extract book title from <h1> tag
        h1_tag = soup.find('h1')
        book_title = h1_tag.get_text(strip=True) if h1_tag else 'Unknown Book'
        
        # Extract chapter title from <h2> tag
        h2_tag = soup.find('h2')
        chapter_title = h2_tag.get_text(strip=True) if h2_tag else 'Unknown Chapter'
        
        # Find the third table and iterate through its rows
        tables = soup.find_all('table')
        if len(tables) != 3:
            print(f'{file_path} - len(tables) == {len(tables)}, not 3 as expected. skipping file.')
            return verse_lines

        third_table = tables[2]
        rows = third_table.find_all('tr')
        
        for row_index, row in enumerate(rows):
            cells = row.find_all('td')
            if len(cells) != 4:
                print(f'{file_path} - ndx:{row_index}, len(cells) == {len(cells)}, not 4 as expected. skipping row.')
                continue

            # Extract data from the four columns
            new_georgian_verse = cells[0].get_text(strip=True)
            new_georgian_text = cells[1].get_text(strip=True)
            old_georgian_verse = cells[2].get_text(strip=True)
            old_georgian_text = cells[3].get_text(strip=True)

            line = [book_title, chapter_title, row_index, new_georgian_verse, new_georgian_text, old_georgian_verse, old_georgian_text]
            verse_lines.append(line)

        return verse_lines


if __name__ == '__main__':
    all_verse_lines = []
    for filename in os.listdir('html_pages'):
        if filename.endswith('.html'):
            file_path = os.path.join('html_pages', filename)
            file_verse_lines = parse_file(file_path)
            all_verse_lines.extend(file_verse_lines)

    with open('parsed_verses.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(all_verse_lines)
