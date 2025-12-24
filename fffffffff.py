mass = {'movies':[{"price": 1}, {"price": 2}, {"price": 3}]}

min = 1
max = 4
avg = 2

# assert response_data["movies"][0]["price"] >= data_for_filter[0]

# for i in m["movies"]:
#     print(i)

assert all(i["price"] >= min for i in mass["movies"]), "Фильтр не работает"
assert all(i["price"] <= max for i in mass["movies"]), "Фильтр не работает"
i




