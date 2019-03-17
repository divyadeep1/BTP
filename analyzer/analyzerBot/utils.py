from django.core.files import File


def save_file(review, filename):
    file_handle = open(filename, 'rb')
    review.file = File(file_handle)
    review.save()
    file_handle.close()
    return True

