from google.appengine.ext import ndb
import webapp2
import json
import string

class Job(ndb.Model):
	id = ndb.StringProperty()
	link = ndb.StringProperty()
	name = ndb.StringProperty()
	start_date = ndb.StringProperty()
	end_date = ndb.StringProperty()
	location = ndb.StringProperty()
	job_type = ndb.StringProperty()

class Employee(ndb.Model):
	id = ndb.StringProperty()
	link = ndb.StringProperty()
	name = ndb.StringProperty()
	contact_number = ndb.StringProperty()
	wage = ndb.StringProperty()
	position = ndb.StringProperty()
	jobs = ndb.KeyProperty(kind=Job, repeated=True)
	def custom_to_dict(self, x):
		r = {}
		r['id'] = self.id
		r['link'] = self.link
		r['name'] = self.name
		r['contact_number'] = self.contact_number
		r['wage'] = self.wage
		r['position'] = self.position
		if x == True:
			r['jobs'] = [Job.query(Job.key == key).get().to_dict() for key in self.jobs]
			return r
		else:
			return r

class EmployeeHandler(webapp2.RequestHandler):
	def post(self):
		try:
			employee_parent_key = ndb.Key(Employee, "parent_employee")
			employee_data = json.loads(self.request.body)
			employee_key = Employee(name=employee_data['name'], contact_number=employee_data['contact_number'], position=employee_data['position'], wage=employee_data['wage'], parent=employee_parent_key).put()
			employee = employee_key.get()
			employee.id = employee_key.urlsafe()
			employee.link = "/employee/" + employee_key.urlsafe()
			employee.put()
			self.response.set_status(201)
			self.response.write(json.dumps(employee_key.get().to_dict()))
		except:
			self.abort(400)

	def get(self, id=None):
		if id:
			self.response.write(json.dumps(ndb.Key(urlsafe=id).get().custom_to_dict(True)))
		else:
			employees = Employee.query().fetch()
			res = []
			for emps in employees:
				res.append(emps.custom_to_dict(False))
			res2 = {}
			res2['employees'] = res
			self.response.write(json.dumps(res2))

	def patch(self, emp_id=None):
		if emp_id:
			emp = ndb.Key(urlsafe=emp_id).get()
			req_data = json.loads(self.request.body)
			if 'name' in req_data:
				emp.name = req_data['name']
			if 'contact_number' in req_data:
				job.contact_number = req_data['contact_number']
			if 'position' in req_data:
				job.position = req_data['position']
			if 'wage' in req_data:
				job.wage = req_data['wage']
			t = {}
			t['name'] = emp.name
			t['id'] = emp.id
			t['contact_number'] = emp.contact_number
			t['position'] = emp.position
			t['wage'] = emp.wage
			t['link'] = emp.link
			emp.put()
			self.response.set_status(201)
			self.response.write(json.dumps(t))

	def delete(self, id=None):
		if id:
			delete_emp = ndb.Key(urlsafe=id).get().to_dict()
			de_jobs = delete_emp['jobs']
			for de in de_jobs:
				de.delete()
			ndb.Key(urlsafe=id).delete()
		else:
			self.abort(401)

class JobHandler(webapp2.RequestHandler):
	def post(self, id=None):
		if id:
			emp_key = ndb.Key(urlsafe=id)
			emp = emp_key.get()
			rq_data = json.loads(self.request.body)
			job_key = Job(name=rq_data['name'], start_date=rq_data['start_date'], end_date=rq_data['end_date'], location=rq_data['location'], job_type=rq_data['job_type']).put()
			job = job_key.get()
			job.id = job_key.urlsafe()
			job.link = str("/employee/job/" + job.id)
			job.put()
			emp.jobs.append(job_key)
			emp.put()
			self.response.set_status(201)
			self.response.write(json.dumps(job_key.get().to_dict()))
		else:
			self.abort(400)

	def patch(self, job_id=None):
		if job_id:
			#emp = ndb.Key(urlsafe=emp_id).get().to_dict()
			job = ndb.Key(urlsafe=job_id).get()
			req_data = json.loads(self.request.body)
			if 'name' in req_data:
				job.name = req_data['name']
			if 'start_date' in req_data:
				job.start_date = req_data['start_date']
			if 'end_date' in req_data:
				job.end_date = req_data['end_date']
			if 'job_type' in req_data:
				job.job_type = req_data['job_type']
			if 'location' in req_data:
				job.location = req_data['location']
			job.put()
			self.response.set_status(201)
			self.response.write(json.dumps(ndb.Key(urlsafe=job_id).get().to_dict()))

	def delete(self, id=None):
		if id:
			ndb.Key(urlsafe=id).delete()	
		else:
			self.abort(401)


allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods
app = webapp2.WSGIApplication([
	('/employee', EmployeeHandler),
	('/employee/(.*)/job', JobHandler),
	('/employee/job/(.*)', JobHandler),
	('/employee/(.*)', EmployeeHandler)
], debug=True)