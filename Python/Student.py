#@author Kowshick Srinivasan
#@version: 1.0
#@Assignment: Hw2
class Student:
    def __init__(self, school,
                 sex,
                 age,
                 address,
                 fam_size,
                 p_status,
                 medu,
                 fedu,
                 m_job,
                 f_job,
                 reason,
                 guardian,
                 travel_time,
                 study_time,
                 failures,
                 schools_up,
                 farms_up,
                 paid,
                 activities,
                 nursery,
                 higher,
                 internet,
                 romantic,
                 fam_rel,
                 free_time,
                 go_out,
                 dalc,
                 walc,
                 health,
                 absence,
                 passed):
        self.school = school
        self.sex = sex
        self.age = age
        self.address = address
        self.fam_size = fam_size
        self.p_status = p_status
        self.medu = medu
        self.fedu = fedu
        self.m_job = m_job
        self.f_job = f_job
        self.reason = reason
        self.guardian = guardian
        self.travel_time = travel_time
        self.study_time = study_time
        self.failures = failures
        self.schools_up = schools_up
        self.farms_up = farms_up
        self.paid = paid
        self.activities = activities
        self.nursery = nursery
        self.higher = higher
        self.internet = internet
        self.romantic = romantic
        self.fam_rel = fam_rel
        self.free_time = free_time
        self.go_out = go_out
        self.dalc = dalc
        self.walc = walc
        self.health = health
        self.absence = absence
        self.passed = passed

    def __str__(self):
        return [self.school, self.sex, self.age, self.address, self.fam_size, self.p_status, self.medu, self.fedu,
                self.m_job, self.f_job, self.reason, self.guardian, self.travel_time, self.study_time, self.failures,
                self.convert_bool_to_string(self.schools_up), self.convert_bool_to_string(self.farms_up), self.convert_bool_to_string(self.paid),
                self.convert_bool_to_string(self.activities), self.convert_bool_to_string(self.nursery), self.convert_bool_to_string(self.higher),
                self.convert_bool_to_string(self.internet),self.convert_bool_to_string(self.romantic), self.fam_rel, self.free_time, self.go_out,
                self.dalc, self.walc, self.health, self.absence,self.convert_bool_to_string(self.passed)]

    def __eq__(self, obj):
        if not isinstance(obj, Student):
            return False
        return (self.school == obj.school and
                self.sex == obj.sex and
                self.age == obj.age and
                self.address == obj.address and
                self.fam_size == obj.fam_size and
                self.p_status == obj.p_status and
                self.medu == obj.medu and
                self.fedu == obj.fedu and
                self.m_job == obj.m_job and
                self.f_job == obj.f_job and
                self.reason == obj.reason and
                self.guardian == obj.guardian and
                self.travel_time == obj.travel_time and
                self.study_time == obj.study_time and
                self.failures == obj.failures and
                self.schools_up == obj.schools_up and
                self.farms_up == obj.farms_up and
                self.paid == obj.paid and
                self.activities == obj.activities and
                self.nursery == obj.nursery and
                self.internet == obj.internet and
                self.higher == obj.higher and
                self.romantic == obj.romantic and
                self.fam_rel == obj.fam_rel and
                self.free_time == obj.free_time and
                self.go_out == obj.go_out and
                self.dalc == obj.dalc and
                self.walc == obj.walc and
                self.health == obj.health and
                self.absence == obj.absence and
                self.passed == obj.passed)

    def convert_bool_to_string(self, boolean_variable):
        if boolean_variable:
            return "yes"
        else:
            return "no"
