from core.exercises.a2_exercises import A2Flexor, A2Extensor
from core.exercises.a3_exercises import A3HandToLumbarSpine, A3ShoulderFlexion090, A3PronationSupinationElbow90
from core.exercises.a4_exercises import A4ShoulderAbduction090, A4ShoulderFlexion90180, A4PronationSupinationElbow0

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
        elif exercise_id == "a_3_hand-to-lumbar-spine":
            return A3HandToLumbarSpine(config)
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
            
        # Legacy support
        elif exercise_id in ["a_4_shoulder_abduction", "shoulder_abduction_copy"]:
            return A4ShoulderAbduction090(config)
        
        # Default fallback - if we don't have a specific implementation,
        # use base class (though it will raise NotImplementedError when evaluated)
        from core.exercises.base import Exercise
        return Exercise(config)