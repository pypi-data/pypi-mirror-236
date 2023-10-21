
from ciocore.validator import Validator
import logging

logger = logging.getLogger(__name__)

class ValidateScoutFrames(Validator):
    def run(self, _):
        """
        Add a validation warning for a potentially costly scout frame configuration.
        """
        try:
            kwargs = self._submitter
            use_scout_frames = kwargs.get("use_scout_frames")
            chunk_size = kwargs.get("chunk_size")

            if chunk_size > 1 and use_scout_frames:
                msg = "You have chunking set higher than 1."
                msg += " This can cause more scout frames to be rendered than you might expect."
                self.add_warning(msg)

        except Exception as e:
            logger.debug("ValidateScoutFrames: {}".format(e))


class ValidateGPURendering(Validator):
    def run(self, _):
        """
        Add a validation warning for a using CPU rendering with Eevee.
        """
        try:
            kwargs = self._submitter
            instance_type_family = kwargs.get("instance_type")
            driver_software = kwargs.get("render_software")
            if "eevee" in driver_software.lower() and "cpu" in instance_type_family.lower():
                msg = "CPU rendering is selected."
                msg += " We strongly recommend selecting GPU rendering when using Blender’s render engine, Eevee."
                self.add_warning(msg)
        except Exception as e:
            logger.debug("ValidateGPURendering: {}".format(e))



# Implement more validators here
####################################


def run(kwargs):
    errors, warnings, notices = [], [], []

    er, wn, nt = _run_validators(kwargs)

    errors.extend(er)
    warnings.extend(wn)
    notices.extend(nt)

    return errors, warnings, notices

def _run_validators(kwargs):


    validators = [plugin(kwargs) for plugin in Validator.plugins()]
    logger.debug("Validators: %s", validators)
    for validator in validators:
        validator.run(kwargs)

    errors = list(set.union(*[validator.errors for validator in validators]))
    warnings = list(set.union(*[validator.warnings for validator in validators]))
    notices = list(set.union(*[validator.notices for validator in validators]))
    return errors, warnings, notices


