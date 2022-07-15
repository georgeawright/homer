(define unidimensional-location-space-parent-concept
  (def-concept :name "" :is_slot True))
(define unidimensional-location-space
  (def-conceptual-space :name "" :parent_concept unidimensional-location-space-parent-concept
    :possible_instances
    (StructureCollection north-south-space west-east-space nw-se-space ne-sw-space)
    :no_of_dimensions 1))
(define location-relation-concept
  (def-concept :name "" :is_slot True :parent_space more-less-space
    :locations (list (Location (list) more-less-space))))
(define label-parent-concept
  (def-concept :name "" :is_slot True :parent_space unidimensional-location-space
    :locations (list (Location (list (list Nan)) unidimensional-location-space))))
(def-relation :start label-parent-concept :end location-relation-concept
  :parent_concept more-concept :activation 1.0)
(define early-time-concept
  (def-concept :name "" :is_slot True :parent_space time-space))
(define late-time-concept
  (def-concept :name "" :is_slot True :parent_space time-space))

(define pp-allative-location-input
  (def-contextual-space :name "pp[location-wards].meaning" :parent_concept input-concept
    :conceptual_spaces (StructureCollection unidimensional-location-space
					    location-space time-space)))
(define pp-allative-location-output
  (def-contextual-space :name "pp[location-wards].text" :parent_concept text-concept
    :conceptual_spaces (StructureCollection grammar-space unidimensional-location-space
					    location-space time-space)))
(define pp-allative-location
  (def-frame :name "pp[location-wards]"
    :parent_concept pp-allative-location-concept
    :parent_frame None
    :sub_frames (StructureCollection)
    :concepts (StructureCollection early-time-concept late-time-concept
				   label-parent-concept location-relation-concept)
    :input_space pp-allative-location-input
    :output_space pp-allative-location-output))

(define early-chunk
  (def-chunk :locations (list (Location (list (list Nan Nan)) location-space)
			      (Location (list (list Nan)) time-space)
			      (Location (list) pp-allative-location-input))
    :parent_space pp-allative-location-input))
(define late-chunk
  (def-chunk :locations (list (Location (list (list Nan Nan)) location-space)
			      (Location (list (list Nan)) time-space)
			      (Location (list) pp-allative-location-input))
    :parent_space pp-allative-location-input))
(define early-chunk-time-label
  (def-label :start early-chunk :parent_concept early-time-concept
    :locations (list (Location (list (list Nan)) time-space)
		     (Location (list) pp-allative-location-input))
    :parent_space pp-allative-location-input))
(define late-chunk-time-label
  (def-label :start late-chunk :parent_concept late-time-concept
    :locations (list (Location (list (list Nan)) time-space)
		     (Location (list) pp-allative-location-input))
    :parent_space pp-allative-location-input))
(define time-relation
  (def-relation :start early-chunk :end late-chunk :parent_concept less-concept
    :quality 1.0
    :locations (list (Location (list (list Nan)) more-less-space)
		     (TwoPointLocation (list (list Nan)) (list (list Nan)) time-space)
		     (TwoPointLocation (list) (list) pp-allative-location-input))
    :conceptual_space time-space))
(define location-relation
  (def-relation :start early-chunk :end late-chunk :parent_concept location-relation-concept
    :locations (list (Location (list (list Nan)) more-less-space)
		     (TwoPointLocation
		      (list (list Nan)) (list (list Nan)) unidimensional-location-space)
		     (TwoPointLocation (list) (list) pp-allative-location-input))
    :conceptual_space unidimensional-location-space))

(define location-chunk
  (def-letter-chunk :name None
    :locations (list (Location (list (list Nan Nan)) location-space)
		     pp-location
		     (Location (list) pp-allative-location-output))
    :parent_space pp-allative-location-output))
(define location-chunk-grammar-label
  (def-label :start location-chunk :parent_concept pp-allative-concept
    :locations (list pp-location
		     (Location (list) pp-allative-location-output))))
(define location-chunk-meaning-label
  (def-label :start location-chunk :parent_concept label-parent-concept
    :locations (list (Location (list (list Nan)) unidimensional-location-space)
		     (Location (list) pp-allative-location-output))))
(define wards-chunk
  (def-letter-chunk :name None
    :locations (list (Location (list (list Nan)) location-space)
		     pp-location
		     (Location (list) pp-allative-location-output))
    :parent_space pp-allative-location-output))
(define wards-chunk-relation
  (def-relation :start location-chunk :end wards-chunk :parent_concept pp-allative-concept
    :locations (list (Location (list) grammar-space)
		     (Location (list) pp-allative-location-output))))
(define pp-allative-super-chunk
  (def-letter-chunk :name None
    :locations (list (Location (list (list Nan Nan)) location-space)
		     pp-location
		     (Location (list) pp-allative-location-output))
    :parent_space pp-allative-location-output
    :left_branch (StructureCollection location-chunk)
    :right_branch (StructureCollection wards-chunk)))
(define pp-allative-super-chunk-label
  (def-label :start pp-allative-super-chunk :parent_concept pp-allative-location-concept
    :locations (list pp-location
		     (Location (list) pp-allative-location-output))))

(def-relation :start label-concept :end pp-allative-location
  :is_bidirectional True :activation 1.0)
(def-relation :start chunk-concept :end pp-allative-location
  :is_bidirectional True :activation 1.0)
(def-relation :start letter-chunk-concept :end pp-allative-location
  :is_bidirectional True :activation 1.0)
(def-relation :start pp-concept :end pp-allative-location
  :is_bidirectional True :activation 1.0)
