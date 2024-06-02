from fuzzywuzzy import fuzz

def find_entities_wrt_eng(en_tr_entities, tr_text):
    # for en_entity_text, tr_entity_text, entity_name in en_tr_entities.items():
    #     if tr_entity_text in tr_text:
    positions = []
    for entity in en_tr_entities:
        tr_entity_text = entity['tr_entity_text']
        start = tr_text.find(tr_entity_text)
        if start != -1:
            end = start + len(tr_entity_text)
            entity['start'] = start
            entity['end'] = end
            # positions.append({"entity": tr_entity_text, "start": start, "end": end})
    # return positions
    return en_tr_entities

def find_similar_entity_positions(tr_text, en_tr_entities, threshold=50):
    positions = []
    for entity in en_tr_entities:
        tr_entity_text = entity['tr_entity_text']
        words = tr_text.split()
        for i, word in enumerate(words):
            text_snippet = ' '.join(words[i:i+len(tr_entity_text.split())])
            similarity = fuzz.ratio(tr_entity_text, text_snippet)
            if similarity >= threshold:
                start = tr_text.find(text_snippet)
                if start != -1:
                    end = start + len(text_snippet)
                    positions.append({
                        "entity": tr_entity_text,
                        "matched_text": text_snippet,
                        "start": start,
                        "end": end,
                        "similarity": similarity
                    })
    return positions

# Function to find similar entities in tr_text
def find_similar_entity_positions_rapid(tr_text, en_tr_entities, threshold=50):
    positions = []
    for entity in en_tr_entities:
        tr_entity_text = entity['tr_entity_text']
        words = tr_text.split()
        for i in range(len(words)):
            for j in range(i + 1, len(words) + 1):
                text_snippet = ' '.join(words[i:j])
                similarity = fuzz.ratio(tr_entity_text, text_snippet)
                if similarity >= threshold:
                    start = tr_text.find(text_snippet)
                    if start != -1:
                        end = start + len(text_snippet)
                        positions.append({
                            "entity": tr_entity_text,
                            "matched_text": text_snippet,
                            "start": start,
                            "end": end,
                            "similarity": similarity
                        })
    return positions

def combine_exact_similarity_search_results(exact_res, similarity_res):
    exact_res_index_finds = [res['tr_entity_text'] for res in exact_res if 'start' in res.keys()]
    distinct_entities_dict = []
    for sim_res in similarity_res:
        if sim_res['entity'] not in exact_res_index_finds:
            distinction_check_flag = distinct_entities_dict and any([True if distinct_entity['entity'] == sim_res['entity'] else False for distinct_entity in distinct_entities_dict])
            if distinction_check_flag:
                #TODO: Fiil this.
            else:
                temp_dict = {
                    'entity': sim_res['entity'],
                    'similarity': sim_res['similarity'],
                    'start': sim_res['start'],
                    'end': sim_res['end'],
                }
                distinct_entities_dict.append(temp_dict)
    print(exact_res)
    print("aaaa")


if __name__ == "__main__":
    en_text = """
    To celebrate the 100th anniversary of the diplomatic relations between Turkey and Japan as well as commemorating 134th anniversary of the Frigate Ertuğrul’s tragic incident off the coast of  Japan, the Turkish Naval Forces 4th and final Ada-class corvette, the TCG Kinaliada (F-514) left Turkey on April 8th and is scheduled to arrive in Japan on June 8th . But before sailing to Japan, the corvette arrived in Hong Kong on 30th May to resupply. The Turkish navy held a press briefing the following day.
    """
    en_shipnames = "TCG Kinaliada"
    en_hn = "F-514"
    en_temp1 = "Frigate Ertuğrul’s"
    tr_shipnames = "TCG Kınalıada"
    tr_hn = "F-514"
    tr_temp1 = "Ertuğrul Fırkateyni"
    # Pattern (en_entity_text, tr_entity_text, en_entity_name)
    en_tr_entities = [("134th anniversary", "134. yıl dönümü", ""),("Turkish Naval Force", "Türk Deniz Kuvvetleri"), ("Ada-class corvette", "Ada sınıfı korvet"), ("F-514", "F-514"), ("TCG Kinaliada", "TCG Kınalıada"), ("Frigate Ertuğrul’s", "Ertuğrul Fırkateyni")]

    tr_text = """
    Türkiye ile Japonya arasındaki diplomatik ilişkilerin 100'üncü yılını kutlamak ve Ertuğrul Fırkateyni'nin Japonya açıklarında yaşadığı trajik olayın 134'üncü yılını kutlamak amacıyla Türk Deniz Kuvvetleri'ne ait 4'üncü ve son Ada sınıfı korvet TCG Kınalıada (F-514) ) 8 Nisan'da Türkiye'den ayrıldı ve 8 Haziran'da Japonya'ya varması planlanıyor. Ancak korvet Japonya'ya doğru yola çıkmadan önce ikmal için 30 Mayıs'ta Hong Kong'a geldi. Türk donanması ertesi gün bir basın toplantısı düzenledi.
    """
    en_tr_entities = [
        {"en_entity_text": "134th anniversary", "tr_entity_text": "134. yıl dönümü", "en_entity_name": "abc"},
        {"en_entity_text": "Turkish Naval Force", "tr_entity_text": "Türk Deniz Kuvvetleri", "en_entity_name": "ccc"},
        {"en_entity_text": "Ada-class corvette", "tr_entity_text": "Ada sınıfı korvet", "en_entity_name": "ddd"},
        {"en_entity_text": "F-514", "tr_entity_text": "F-514", "en_entity_name": "sss"},
        {"en_entity_text": "TCG Kinaliada", "tr_entity_text": "TCG Kınalıada", "en_entity_name": "fff"},
        {"en_entity_text": "Frigate Ertuğrul’s", "tr_entity_text": "Ertuğrul Fırkateyni", "en_entity_name": "hhh"}
    ]

    exact_match_res = find_entities_wrt_eng(en_tr_entities, tr_text)
    print(exact_match_res)
    #
    # for entity_res in res:
    #     print(tr_text[entity_res["start"]:entity_res["end"]], entity_res["entity"])

    positions = find_similar_entity_positions(tr_text, en_tr_entities)
    print(positions)

    similarity_based_search = find_similar_entity_positions_rapid(tr_text, en_tr_entities)
    print(similarity_based_search)

    combine_exact_similarity_search_results(exact_res=exact_match_res, similarity_res=similarity_based_search)


