from dockerstack.Platform import Platform


class Default(Platform):

    def pre_processing(self):
        print 'Nothing to update'
        return

    def post_processing(self):
        print 'No scripts after run'
        return
