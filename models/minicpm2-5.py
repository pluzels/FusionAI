import json
import g4f

def generate_response(prompt):
    try:
        # panggil api g4f untuk mendapatkan response
        response = g4f.ChatCompletion.create(
            model='minicpm-2.5',
            provider=g4f.Provider.DeepInfraChat,
            messages=[
                {"role": "system", "content": "you are a helpful assistant."},
                {"role": "user", "content": prompt},
            ]
        )
    except Exception as e:
        return {"response": f"error: exception saat memanggil g4f: {str(e)}"}

    print("raw response:", response)  # debug: lihat apa yang dikembalikan

    try:
        # jika response adalah string, coba parse json-nya
        if isinstance(response, str):
            try:
                parsed_response = json.loads(response)
            except json.JSONDecodeError:
                # jika gagal parse, anggap response itu teks biasa
                return {"response": response}
        else:
            parsed_response = response

        # pastikan parsed_response merupakan dict dengan key 'choices'
        if isinstance(parsed_response, dict) and "choices" in parsed_response:
            choices = parsed_response["choices"]
            if isinstance(choices, list) and len(choices) > 0:
                first_choice = choices[0]
                if "message" in first_choice and "content" in first_choice["message"]:
                    return {"response": first_choice["message"]["content"]}
                else:
                    return {"response": "error: key 'message' atau 'content' tidak ditemukan di response"}
            else:
                return {"response": "error: 'choices' kosong atau tidak berbentuk list"}
        else:
            return {"response": "error: format response tidak sesuai, tidak ada key 'choices'"}
    except Exception as e:
        return {"response": f"error: exception saat memproses response: {str(e)}"}
