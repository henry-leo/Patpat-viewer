import finisher

condition = {'start': '2012', 'end': '2013', 'databases': [], 'keywords': []}

data_imported = finisher.ImportFinisher('3d5b4e1d-937c-4661-83a2-b6ed7c19f060').run()
acc_filtered = finisher.FiltrateFinisher(
    datasets=data_imported,
    condition=condition
).run()
