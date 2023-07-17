(define space-parent-concept
  (def-concept :name "" :is_slot True))
(define conceptual-space
  (def-conceptual-space :name "" :parent_concept space-parent-concept
    :possible_instances (StructureSet temperature-space height-space goodness-space)
    :no_of_dimensions 1))
(define label-parent-concept
  (def-concept :name "" :is_slot True :parent_space conceptual-space
    :locations (list (Location (list (list Nan)) conceptual-space))))
(define relation-parent-concept
  (def-concept :name "" :is_slot True :parent_space more-less-space
    :locations (list (Location (list) more-less-space))))
(def-relation :start label-parent-concept :end relation-parent-concept
  :parent_concept more-concept :activation 1.0)
(define similarity-space-parent-concept
  (def-concept :name "" :is_slot True))
(define similarity-space
  (def-conceptual-space :name "" :parent_concept similarity-space-parent-concept
    :possible_instances (StructureSet time-space location-space)
    :no_of_dimensions Nan))

(define rp-input
  (def-contextual-space :name "rp[jjr].meaning" :parent_concept input-concept
    :conceptual_spaces (StructureSet conceptual-space)))
(define rp-output
  (def-contextual-space :name "rp[jjr].text" :parent_concept text-concept
    :conceptual_spaces (StructureSet grammar-space conceptual-space)))
(define rp-frame
  (def-frame :name "rp[jjr]"
    :parent_concept rp-concept :parent_frame None
    :sub_frames (StructureSet)
    :concepts (StructureSet label-parent-concept relation-parent-concept)
    :input_space rp-input :output_space rp-output))

(define chunk-start
  (def-chunk :locations (list (Location (list (list Nan)) conceptual-space)
			      (Location (list) rp-input))
    :parent_space rp-input))
(define chunk-end
  (def-chunk :locations (list (Location (list (list Nan)) conceptual-space)
			      (Location (list) rp-input))
    :parent_space rp-input))
(define chunk-start-label
  (def-label :start chunk-start :parent_concept label-parent-concept
    :locations (list (Location (list (list Nan)) conceptual-space)
		     (Location (list) rp-input))))
(define comparative-relation
  (def-relation :start chunk-start :end chunk-end :parent_concept relation-parent-concept
    :quality 1.0
    :locations (list (Location (list (list Nan)) more-less-space)
		     (TwoPointLocation (list (list Nan)) (list (list Nan)) conceptual-space)
		     (TwoPointLocation (list) (list) rp-input))
    :conceptual_space conceptual-space))
(define sameness-relation
  (def-relation :start chunk-start :end chunk-end :parent_concept same-concept
    :quality 1.0
    :locations (list (Location (list (list Nan)) same-different-space)
		     (TwoPointLocation (list (list)) (list (list)) similarity-space)
		     (TwoPointLocation (list (list)) (list (list)) rp-input))
    :conceptual_space similarity-space))

(define jjr-chunk
  (def-letter-chunk :name None
    :locations (list (Location (list (list Nan)) conceptual-space)
		     jjr-location
		     (Location (list) rp-output))
    :parent_space rp-output))
(define er-chunk
  (def-letter-chunk :name None
    :locations (list (Location (list (list Nan)) conceptual-space)
		     jjr-location
		     (Location (list) rp-output))
    :parent_space rp-output))
(define jjr-super-chunk
  (def-letter-chunk :name None
    :locations (list (Location (list (list Nan)) conceptual-space)
		     rp-location
		     (Location (list) rp-output))
    :parent_space rp-output
    :left_branch (StructureSet jjr-chunk)
    :right_branch (StructureSet er-chunk)))
(define jjr-chunk-grammar-label
  (def-label :start jjr-chunk :parent_concept jjr-concept
    :locations (list jjr-location
		     (Location (list) rp-output))))
(define jjr-chunk-meaning-label
  (def-label :start jjr-chunk :parent_concept label-parent-concept
    :locations (list (Location (list (list Nan)) conceptual-space)
		     (Location (list) rp-output))))
(define er-chunk-relation
  (def-relation :start jjr-chunk :end er-chunk :parent_concept jjr-concept
    :locations (list (Location (list) grammar-space)
		     (Location (list) rp-output))))
(define jjr-super-chunk-label
  (def-label :start jjr-super-chunk :parent_concept rp-concept
    :locations (list rp-location
		     (Location (list) rp-output))))

(def-relation :start more-temperature-concept :end rp-frame
  :is_bidirectional True :stable_activation 1.0)
(def-relation :start more-height-concept :end rp-frame
  :is_bidirectional True :stable_activation 1.0)
(def-relation :start more-goodness-concept :end rp-frame
  :is_bidirectional True :stable_activation 1.0)
