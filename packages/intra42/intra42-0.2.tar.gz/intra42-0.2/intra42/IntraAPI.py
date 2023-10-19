import requests
from time import sleep
import datetime
import os
import typing
import json

T = typing.TypeVar('T')
API_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

class Token:
	def __init__(self, token_42:str):
		self.token_42 = token_42
		self.time = datetime.datetime.fromtimestamp(0)

	def is_ready(self):
		return datetime.datetime.now() - self.time >= datetime.timedelta(seconds=0.5)
	
	def elapsed(self):
		return (datetime.datetime.now() - self.time).total_seconds()

	def get_token(self):
		self.time = datetime.datetime.now()
		return self.token_42

class UserImageVersion(typing.TypedDict):
	large:str
	medium:str
	small:str
	micro:str

class UserImage(typing.TypedDict):
	link:str
	versions:UserImageVersion

class User(typing.TypedDict):
	id: int
	email: str
	login: str
	first_name: str
	last_name: str
	usual_full_name: str
	usual_first_name: str
	url: str
	phone: str
	displayname: str
	kind: str
	image: UserImage
	staff: bool
	correction_point: int
	pool_month: str
	pool_year: str
	location: str
	wallet: int
	anonymize_date: str
	data_erasure_date: str
	created_at: str
	updated_at: str
	alumnized_at: str
	alumni: bool
	active: bool

class Feedback(typing.TypedDict):
	comment: str
	rating: int

class Cursus(typing.TypedDict):
	start:datetime.datetime
	end:datetime.datetime
	id:int

class Grade(typing.TypedDict):
	begin_at:datetime.datetime
	filled_at:datetime.datetime
	cursus_id:int
	comment:str
	grade:int
	corrector:str
	feedback:Feedback

trans = str.maketrans({
	'{':'', '}':'',
	'\'':'',
	'\"':'',
	' ':'',

	':':'_',
	',':'_',
	'.':'_',
	'/':'_'
	})
class IntraAPI:

	def __init__(self, ids:list, json_save_folder:str="tmp_data"):
		self.ids = ids
		self.json_save_folder = json_save_folder
		self.tokens:typing.List[Token]
		self.tokens = []

	def get_tokens(self):
		for i, id in enumerate(self.ids):
			try:
				x = requests.post("https://api.intra.42.fr/oauth/token",
						json={ "grant_type":"client_credentials", "client_id":id[0], "client_secret":id[1] }).json()
			except Exception as e:
				print(f"An error occured while retrieving the token {i}:")
				print(f"Request:\n{x}")
				print(f"Exception:\n{e}\n")
				continue
			if ("error" in x):
				print(f"An error occured while retrieving the token {i}:")
				print(f"Request:\n{x}")
				print(f"Exception:\n{x['error']} : {x['error_description']}\n")
				continue

			try:
				token = x["access_token"]
				self.tokens.append(Token(token))
			except:
				print(f"An error occured while retrieving the token {i}:")
				print(f"Request:\n{x}")
				print(f"Exception:\n{e}")
				continue

	def json_path(self, url:str, id=None) -> str:
		path = self.json_save_folder + url.removeprefix('http://').removeprefix('https://')
		if (id):
			path += f"_{id}"
		return path.translate(trans)

	def create_file_for_url(self, url:str, id:str=None) -> typing.IO:
		if (not os.path.isdir(self.json_save_folder)):
			os.mkdir(self.json_save_folder)
		return open(self.json_path(url, id), 'w+')

	def make_json_request(self, method, url:str, *args, update=False, path_id:str=None, retry=0, **kwargs) -> dict:
		if (not update):
			try:
				try:
					f_time = datetime.datetime.fromtimestamp(os.path.getmtime(self.json_path(url, path_id)))
					if (f_time - datetime.datetime.now() >= datetime.timedelta(days=1)):
						raise Exception("File too old")
				except FileNotFoundError as e:
					pass

				f = open(self.json_path(url, path_id), 'r')
				data = json.load(f)
				f.close()

				return data
			except (FileNotFoundError, FileExistsError, json.JSONDecodeError) as e:
				pass

		for t in self.tokens:
			if (t.is_ready()):
				print()
				headers = kwargs.pop("headers", {})
				headers.update({"Authorization":"Bearer " + t.get_token()})
				resp = method(url, *args, **kwargs, headers=headers)
				try:
					data = resp.json()
					if (len(data) != 0):
						f = IntraAPI.create_file_for_url(url, path_id)
						json.dump(data, f, indent=4)
						f.close()
				except Exception as e:
					return None
				return data
		print(f"Retry {retry}...", end='\r')
		sleep(0.1)
		return self.make_request(method, *args, retry=retry+1, **kwargs)

	def make_request(self, method: typing.Callable[..., T], *args, retry=0, **kwargs) -> T:
		for t in self.tokens:
			if (t.is_ready()):
				headers = kwargs["headers"] if kwargs.get("headers") else {}
				headers.update({"Authorization":"Bearer " + t.get_token()})
				return method(*args, **kwargs)
		sleep(0.1)
		return self.make_request(method, *args, retry=retry+1, **kwargs)

def get_all_pages(apiintra:IntraAPI, url:str, *args, id:str="", **kwargs):
	result = []
	x = [1]
	params:dict = kwargs.pop("params", {})
	if ("page[size]" not in params):
		params["page[size]"] = 100
	page = params.get("page[number]", 1)

	while (len(x) != 0):
		params["page[number]"] = page
		x=apiintra.make_json_request(requests.get,
			url,
			*args,
			params=params,
			path_id=f"{id}_page{page}"
		)
		if (len(x) != 0):
			result += x
		page += 1
	return result

def get_42mulhouse_users(apiintra:IntraAPI, filters={})->typing.List[User]:
	print("Retrieving all 42 Mulhouse's users...")
	params = {
		"filter[primary_campus_id]": 48,
		"filter[kind]": "student",
		"page[size]": 100
	}
	params.update(filters)
	users = [u for u in get_all_pages(apiintra, "https://api.intra.42.fr/v2/users", id=json.dumps(params), params=params) if u["active?"]]
	return users

def get_all_scales(apiintra:IntraAPI, user_id, filters={})->list:
	scales = [u for u in get_all_pages(apiintra, f"https://api.intra.42.fr/v2/users/{user_id}/scale_teams") if u["active?"]]
	return scales

def get_user_info(apiintra:IntraAPI, user_id):
	x=apiintra.make_request(requests.get, f"https://api.intra.42.fr/v2/users/{user_id}")
	return x.json()

