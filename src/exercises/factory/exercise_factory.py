from src.exercises.implementations.a2.exercises import A2Flexor, A2Extensor
from src.exercises.implementations.a3.exercises import A3ShoulderFlexion090, A3PronationSupinationElbow90
from src.exercises.implementations.a4.exercises import A4ShoulderAbduction090, A4ShoulderFlexion90180, A4PronationSupinationElbow0
from src.exercises.implementations.c.exercises import CFlexion, CExtension
from src.exercises.implementations.d.exercises import DNoseKnee
from src.exercises.base.base_exercise import Exercise

class ExerciseFactory:
    @staticmethod
    def create_exercise(config):
        """
        Create an exercise instance based on the exercise ID
        """
        exercise_id = config.get("id", "")
        
        # A2 exercises
        if exercise_id == "a_2_flexor":
            return A2Flexor(config)
        elif exercise_id == "a_2_extensor":
            return A2Extensor(config)
            
        # A3 exercises
        elif exercise_id == "a_3_shoulder-flexion-0-90":
            return A3ShoulderFlexion090(config)
        elif exercise_id == "a_3_pronation-supination-elbow-90":
            return A3PronationSupinationElbow90(config)
            
        # A4 exercises
        elif exercise_id == "a_4_shoulder-abduction-0-90":
            return A4ShoulderAbduction090(config)
        elif exercise_id == "a_4_shoulder-flexion-90-180":
            return A4ShoulderFlexion90180(config)
        elif exercise_id == "a_4_pronation-supination-elbow-0":
            return A4PronationSupinationElbow0(config)
        
        # C exercises
        elif exercise_id == "c_flexion":
            return CFlexion(config)
        elif exercise_id == "c_extension":
            return CExtension(config)
            
        # D exercises
        elif exercise_id == "d_nose_knee":
            return DNoseKnee(config)
            
        # Default fallback - if we don't have a specific implementation,
        # use base class (though it will raise NotImplementedError when evaluated)
        return Exercise(config) 