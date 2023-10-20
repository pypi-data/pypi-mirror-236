class SendSMSResponse(object):
    """
    This API is used to send a message to one or more recipients
    """
    JOB_ID = 'jobId'
    TOTAL = 'total'
    REJECTED = 'rejected'
    ACCEPTED = 'accepted'
    DUPLICATES = 'duplicates'
    COST = 'cost'

    def __init__(self, job_id: str, total: int, rejected: int, accepted: int, duplicates: int, cost: int):
        """
        When you create a new object of a class, Python automatically calls the __init__() method to
        initialize the object’s attributes.
        """
        self.job_id = job_id
        self.total = total
        self.rejected = rejected
        self.accepted = accepted
        self.duplicates = duplicates
        self.cost = cost

    def to_dictionary(self):
        """
        Return the property of the object as a dictionary
        """
        return {
            self.JOB_ID: self.job_id,
            self.TOTAL: self.total,
            self.REJECTED: self.rejected,
            self.ACCEPTED: self.accepted,
            self.DUPLICATES: self.duplicates,
            self.cost: self.cost,
        }

    @classmethod
    def form_dictionary(cls, dictionary: dict):
        """
        Creates an instance of this model from a dictionary
        """
        if dictionary is None:
            return None

        # Extract variables from the dictionary
        job_id = dictionary.get(cls.JOB_ID)
        total = dictionary.get(cls.TOTAL)
        rejected = dictionary.get(cls.REJECTED)
        accepted = dictionary.get(cls.ACCEPTED)
        duplicates = dictionary.get(cls.DUPLICATES)
        cost = dictionary.get(cls.COST)

        # Return an object of this model
        return cls(job_id=job_id, total=total, rejected=rejected, accepted=accepted, duplicates=duplicates, cost=cost)
