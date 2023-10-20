from model_bakery import baker


def test_wrapped_subject_str_method():
    subject = baker.prepare('subjects_wrapper.WrappedSubject')

    assert str(subject) == subject.pseudonym
