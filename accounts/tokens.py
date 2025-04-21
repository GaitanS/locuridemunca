from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six # For Python 2/3 compatibility, though likely just 3 now

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # Ensure the hash includes the user's pk, timestamp, and activation status
        # This invalidates the token if the user's status changes after token generation
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )

account_activation_token = AccountActivationTokenGenerator()
