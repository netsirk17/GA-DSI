  # create dictionary for array
  predict_vars = ['age_log', u'total_number_dogs', 'size', 'coat', 'word_name', u'in_sex', 'dark mix', 'in_neuter', \
  'energy', 'cute_name', 'groom', 'Normal', 'Stray', 'light mix', 'popular_shelter_name', 'human_name', \
  'Owner Surrender', 4, 'popular_dog_name', 'sporting', 'herding', 'toy', 'light', 6, 'other', 3, \
  'Public Assist', 11, 'chihuahua', 'aggressive']


  #initialize empty df for predictions
  pred_df = pd.DataFrame(columns=predict_vars)
  pred_df.loc[1,:]=0
  # calculate name related features
  name = dog_name.lower()

  top_dog_names = [u'cookie', u'blue', u'daisy', u'bella', u'rocky', u'jackson', u'king', u'duke', u'roscoe',
     u'lucy', u'chico', u'fiona', u'princess', u'lola', u'monty', u'morgan', u'bailey', u'molly',
     u'luke', u'jack', u'raven', u'max', u'junior', u'sadie', u'reese', u'libby', u'oreo', u'oliver',
     u'honey', u'brownie', u'wally', u'rusty', u'tulip', u'cane', u'hercules', u'lady', u'diesel',
     u'maggie', u'izzy', u'colt', u'earl', u'penny', u'murphy', u'bentley', u'lulu', u'sky', u'zoey',
     u'cooper', u'jazz', u'caleb', u'snowy', u'ellie', u'lily', u'star', u'rosie', u'goldie']
  top_dog_names_shelter = ['bella', 'max', 'daisy', 'charlie', 'rocky', 'princess', 'buddy', 'lucy', 'lucky', 'luna',
             'coco', 'chico', 'lola', 'sadie', 'jack', 'lady', 'blue', 'molly', 'duke', 'toby', 'bear',
             'diamond', 'sasha', 'shadow', 'chloe', 'rosie', 'brownie', 'zeus', 'oso', 'lily', 'ginger',
             'rex', 'marley', 'oreo', 'king', 'cookie', 'buster', 'maggie', 'ruby', 'roxy']

  pred_df["age_log"] = log(age)
  pred_df["total_number_dogs"] = total_number_dogs
  pred_df["in_sex"] = in_sex
  pred_df["in_neuter"] = in_neuter

  if colour in predict_vars:
    pred_df[colour] = 1
  if month in predict_vars:
    pred_df[month] = 1
  if condition in predict_vars:
    pred_df[condition] = 1
  if intake in predict_vars:
    pred_df[intake] = 1

  breed_list = [breed1.lower(), breed2.lower()]
  breed_list = [i for i in breed_list if i!="nobreed"]
  for i in breed_list:
    if i in predict_vars and i != "other":
    pred_df[i] = 1
  akc = pd.read_csv("data/akc.csv")
  akc["breed"] = akc["breed"].apply(lambda x: x.lower())
  akc.set_index("breed", inplace=True)

  aggressive  = ["pit bull","american staffordshire terrier","staffordshire bull terrier"]
  energy_list = []
  size_list = []
  coat_list = []
  groom_list = []

  ave_energy = 2.4
  ave_size = 1.75
  ave_coat = 1.35
  ave_groom = 1.15

  all_breeds = akc.index.values

  for i in breed_list:
  if i in all_breeds:
  energy_list.append(akc.loc[i,"energy"])
  size_list.append(akc.loc[i,"size"])
  coat_list.append(akc.loc[i,"coat"])
  groom_list.append(akc.loc[i,"groom"])
  if i in aggressive:
  pred_df["aggressive"]=1
  if pd.isnull(akc.loc[i,"group"]):
  pred_df["other"] = 1
  else:
  if akc.loc[i,"group"] in predict_vars:
    pred_df[akc.loc[i,"group"]] = 1
  else:
  energy_list.append(ave_energy)
  size_list.append(ave_size)
  coat_list.append(ave_coat)
  groom_list.append(ave_groom)

  pred_df["energy"] = np.mean(energy_list)
  pred_df["size"] = np.mean(size_list)
  pred_df["coat"] = np.mean(coat_list)
  pred_df["groom"] = np.mean(groom_list)

  if name in all_names:
  pred_df["human_name"]=1

  if name in top_dog_names:
  pred_df["popular_dog_name"]=1

  if name in top_dog_names_shelter:
  pred_df["popular_shelter_name"]=1

  def cute_name(x):
  try:
  if x[-2:] =="ee" or x[-2:] =="ie" or x[-2:] =="ey" or x[-1]=="y"or x[-1]=="i":
  return 1
  else:
  return 0
  except:
  return 0
  pred_df["cute_name"] = cute_name(name)

  if name in word_list:
  pred_df["word_name"] = 1

  # predict outcome binary
  pred_array = np.array(pred_df)

  scores = model.predict_proba(pred_array)
  if scores[0][1] >=0.60:
  prediction = 1
  else:
  prediction = 0
  if prediction ==1:
  pred_string = "This dog is likely to be adopted within 8 days."
  else:
  pred_string = "This dog is likely to take longer than 8 days to be adopted."
