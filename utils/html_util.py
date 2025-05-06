from bs4 import BeautifulSoup
def extract_product_info(soup: BeautifulSoup):
    title = None

    title_selectors = [
        '.product-title',
        '.product-name',
        'h1.title',
        'h1',
        '.product-info h1',
        '.product-detail-page h1'
    ]

    for selector in title_selectors:
        title = soup.select_one(selector)
        if title:
            break
    

    return {
        "title": title.text.strip() if title else None,
    }

def extract_attributes(soup):
    
    attributes = {}
    
    # Try multiple possible selectors for attribute sections
    attr_section_selectors = [
        '.module_attribute',
        '#key-attributes',
        '.product-attributes',
        '.product-props',
        '.product-specifications',
        '.specs-module',
        '.attributes-module',
        '.attributes-list',
        '.product-info-attributes',
        '.product-attributes-container',
        'table.attributes-table',
        'div[data-spm="product_detail"] table',
        '.product-detail-attributes'
    ]
    
    attr_section = None
    for selector in attr_section_selectors:
        attr_section = soup.select_one(selector)
        # print(f"Trying selector: {selector} - Found: {bool(attr_section)}")
        if attr_section:
            break
    
    if not attr_section:
        # If we still don't have an attribute section, try to find tables that might contain attributes
        tables = soup.select('table')
        for table in tables:
            # Look for tables that might contain product attributes
            if table.select('th') and table.select('td'):
                attr_section = table
                break
    
    if not attr_section:
        return attributes
    
    # First try to extract attributes from a structured attribute section
    # Find all section headings
    headings = attr_section.select('h3, h4, .section-title, .attribute-section-title')
    
    
    if headings:
        # Process each section
        for heading in headings:
            section_name = heading.text.strip()
            attributes[section_name] = {}
            
            # Find the next attribute list - could be a sibling or a child container
            attr_list = heading.find_next_sibling() or heading.find_next('div', class_=['attribute-list', 'attributes-list'])
            # print("attribute list:", attr_list)
            if attr_list:
                # Try different attribute item selectors
                items = attr_list.select('.attribute-item, .spec-item, .prop-item, tr')
                # print("items:", items)
                
                for item in items:
                    # Try different name-value pair selectors
                    name_el = item.select_one('.left, .name, .spec-name, th, td:first-child')
                    value_el = item.select_one('.right, .value, .spec-value, td:last-child')
                    
                    if name_el and value_el:
                        name = name_el.text.strip()
                        value = value_el.text.strip()
                        attributes[section_name][name] = value
    else:
        # No sections, try to get all attributes directly
        # First check for table-based attributes
        if attr_section.name == 'table' or attr_section.select_one('table'):
            table = attr_section if attr_section.name == 'table' else attr_section.select_one('table')
            attributes['Product Specifications'] = {}
            
            rows = table.select('tr')
            for row in rows:
                cells = row.select('td, th')
                if len(cells) >= 2:
                    name = cells[0].text.strip()
                    value = cells[1].text.strip()
                    if name and value and not name.lower() == 'product specifications':
                        attributes['Product Specifications'][name] = value
        else:
            # Try to find attribute items directly
            attributes['General Attributes'] = {}
            items = attr_section.select('.attribute-item, .spec-item, .prop-item, li')
            
            for item in items:
                # Try different name-value pair selectors
                name_el = item.select_one('.left, .name, .spec-name, .prop-name')
                value_el = item.select_one('.right, .value, .spec-value, .prop-value')
                
                if name_el and value_el:
                    name = name_el.text.strip()
                    value = value_el.text.strip()
                    attributes['General Attributes'][name] = value
    
    # If we still don't have attributes, try a more generic approach
    if not attributes:
        # Look for any div with a label and value structure
        label_value_pairs = soup.select('div.item-title + div.item-value, dt + dd')
        if label_value_pairs:
            attributes['Product Details'] = {}
            for i in range(0, len(label_value_pairs), 2):
                if i + 1 < len(label_value_pairs):
                    name = label_value_pairs[i].text.strip()
                    value = label_value_pairs[i + 1].text.strip()
                    attributes['Product Details'][name] = value
        
        # Try to find any tables with product specs
        spec_tables = soup.find_all('table')
        for table in spec_tables:
            rows = table.find_all('tr')
            if rows:
                table_attrs = {}
                
                for row in rows:
                    cells = row.find_all('td')
                    if len(cells) >= 2:
                        name = cells[0].get_text().strip()
                        value = cells[1].get_text().strip()
                        if name and value:
                            table_attrs[name] = value
                
                if table_attrs:
                    attributes["Product Specifications"] = table_attrs

    return attributes
