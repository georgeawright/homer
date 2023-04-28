(define space-parent-concept
  (def-concept :name "" :is_slot True))
(define conceptual-space
  (def-conceptual-space :name "" :parent_concept space-parent-concept
    :possible_instances (StructureSet temperature-space height-space goodness-space)
    :no_of_dimensions 1))
(define conceptual-label-concept
  (def-concept :name "" :is_slot True :parent_space conceptual-space))
(define location-concept
  (def-concept :name "" :is_slot True :parent_space location-space))
 
(define description-sub-frame-input
  (def-contextual-space :name "description-sub-frame.input" :parent_concept input-concept
    :conceptual_spaces (StructureSet conceptual-space)))
(define description-sub-frame-output
  (def-contextual-space :name "description-sub-frame.text" :parent_concept text-concept
    :conceptual_spaces (StructureSet grammar-space conceptual-space)))
(define description-sub-frame
  (def-sub-frame :name "s-be-ap-sub" :parent_concept ap-concept :parent_frame None
    :sub_frames (StructureSet)
    :concepts (StructureSet conceptual-label-concept)
    :input_space description-sub-frame-input
    :output_space description-sub-frame-output))

(define location-sub-frame-input
  (def-contextual-space :name "location-sub-frame.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureSet location-space)))
(define location-sub-frame-output
  (def-contextual-space :name "location-sub-frame.text" :parent_concept text-concept
    :conceptual_spaces (StructureSet grammar-space location-space)))
(define location-sub-frame
  (def-sub-frame :name "s-be-location-sub"
    :parent_concept pp-inessive-location-concept
    :parent_frame None
    :sub_frames (StructureSet)
    :concepts (StructureSet location-concept)
    :input_space location-sub-frame-input
    :output_space location-sub-frame-output))

(define time-sub-frame-input
  (def-contextual-space :name "time-sub-frame.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureSet time-space)))
(define time-sub-frame-output
  (def-contextual-space :name "time-sub-frame.text" :parent_concept text-concept
    :conceptual_spaces (StructureSet grammar-space time-space)))
(define time-sub-frame
  (def-sub-frame :name "s-be-time-sub"
    :parent_concept pp-directional-time-concept
    :parent_frame None
    :sub_frames (StructureSet)
    :concepts (StructureSet)
    :input_space time-sub-frame-input
    :output_space time-sub-frame-output))

(define be-sentence-input
  (def-contextual-space :name "s-be.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureSet location-space time-space conceptual-space)))
(define be-sentence-output
  (def-contextual-space :name "s-be.text" :parent_concept text-concept
    :conceptual_spaces (StructureSet
			grammar-space verb-space location-space time-space conceptual-space)))
(define be-sentence
  (def-frame :name "s-be" :parent_concept sentence-concept :parent_frame None
    :depth 6
    :sub_frames (StructureSet description-sub-frame location-sub-frame time-sub-frame)
    :concepts (StructureSet location-concept)
    :input_space be-sentence-input
    :output_space be-sentence-output))

(define early-chunk
  (def-chunk :locations (list (Location (list (list Nan Nan)) location-space)
			      (Location (list (list Nan)) time-space)
			      (Location (list (list Nan)) conceptual-space)
			      (Location (list) location-sub-frame-input)
			      (Location (list) time-sub-frame-input)
			      (Location (list) be-sentence-input))
    :parent_space be-sentence-input))
(define early-chunk-least-time-label
  (def-label :start early-chunk :parent_concept least-concept
    :locations (list (Location (list (list Nan)) time-space)
		     (Location (list) be-sentence-input))
    :is_interspatial True
    :quality 1.0 :activation 1.0))
(define early-chunk-conceptual-label
  (def-label :start early-chunk :parent_concept conceptual-label-concept
    :locations (list (Location (list (list Nan)) conceptual-space)
		     (Location (list) description-sub-frame-input)
		     (Location (list) be-sentence-input))
    :parent_space description-sub-frame-input))
(define late-chunk
  (def-chunk :locations (list (Location (list (list Nan Nan)) location-space)
			      (Location (list (list Nan)) time-space)
			      (Location (list (list Nan)) conceptual-space)
			      (Location (list) location-sub-frame-input)
			      (Location (list) time-sub-frame-input)
			      (Location (list) be-sentence-input))
    :parent_space be-sentence-input))
(define late-chunk-most-time-label
  (def-label :start late-chunk :parent_concept most-concept
    :locations (list (Location (list (list Nan)) time-space)
		     (Location (list) be-sentence-input))
    :is_interspatial True
    :quality 1.0 :activation 1.0))
(define late-chunk-location-label
  (def-label :start late-chunk :parent_concept location-concept
    :locations (list (Location (list (list Nan Nan)) location-space)
		     (Location (list) location-sub-frame-input)
		     (Location (list) be-sentence-input))
    :parent_space location-sub-frame-input))

(define time-relation
  (def-relation :start early-chunk :end late-chunk :parent_concept less-concept
    :quality 1.0
    :locations (list (Location (list (list Nan)) more-less-space)
		     (TwoPointLocation (list (list Nan)) (list (list Nan)) time-space)
		     (TwoPointLocation (list) (list) time-sub-frame-input)
		     (TwoPointLocation (list) (list) be-sentence-input))
    :parent_space time-sub-frame-input
    :conceptual_space time-space))
(define location-relation
  (def-relation :start late-chunk :end early-chunk :parent_concept same-concept
    :quality 1.0
    :locations (list (Location (list (list Nan)) same-different-space)
		     (TwoPointLocation (list (list Nan Nan)) (list (list Nan Nan)) location-space)
		     (TwoPointLocation (list) (list) be-sentence-input))
    :parent_space be-sentence-input
    :conceptual_space location-space))
(define conceptual-relation
  (def-relation :start late-chunk :end early-chunk :parent_concept same-concept
    :quality 1.0
    :locations (list (Location (list (list Nan)) same-different-space)
		     (TwoPointLocation (list (list Nan)) (list (list Nan)) conceptual-space)
		     (TwoPointLocation (list) (list) be-sentence-input))
    :parent_space be-sentence-input
    :conceptual_space conceptual-space))

(define sentence-word-1
  (def-letter-chunk :name "temperatures"
    :locations (list nsubj-location
		     (Location (list) be-sentence-output))
    :parent_space be-sentence-output
    :abstract_chunk temperatures))
(define sentence-word-1-label
  (def-label :start sentence-word-1 :parent_concept nsubj-concept
    :locations (list nsubj-location
		     (Location (list) be-sentence-output))))
(define sentence-word-2
  (def-letter-chunk :name "will"
    :locations (list aux-location
		     (Location (list) be-sentence-output))
    :parent_space be-sentence-output
    :abstract_chunk will))
(define sentence-word-3
  (def-letter-chunk :name "be"
    :locations (list vb-location
		     (Location (list) be-sentence-output))
    :parent_space be-sentence-output
    :abstract_chunk be))
(define sentence-word-4
  (def-letter-chunk :name None
    :locations (list ap-location
		     (Location (list) description-sub-frame-output)
		     (Location (list) be-sentence-output))
    :parent_space description-sub-frame-output))
(define description-chunk-grammar-label
  (def-label :start sentence-word-4 :parent_concept ap-concept
    :locations (list ap-location
		     (Location (list) description-sub-frame-output))))
(define sentence-word-5
  (def-letter-chunk :name None
    :locations (list pp-location
		     (Location (list) location-sub-frame-output)
		     (Location (list) be-sentence-output))
    :parent_space location-sub-frame-output))
(define location-chunk-grammar-label
  (def-label :start sentence-word-5 :parent_concept pp-inessive-location-concept
    :locations (list pp-location
		     (Location (list) location-sub-frame-output))))
(define sentence-word-6
  (def-letter-chunk :name None
    :locations (list pp-location
		     (Location (list) time-sub-frame-output)
		     (Location (list) be-sentence-output))
    :parent_space time-sub-frame-output))
(define time-chunk-grammar-label
  (def-label :start sentence-word-6 :parent_concept pp-directional-time-concept
    :locations (list pp-location
		     (Location (list) time-sub-frame-output))))

(define v-super-chunk
  (def-letter-chunk :name None
    :locations (list v-location
		     (Location (list) be-sentence-output))
    :parent_space be-sentence-output
    :left_branch (StructureSet sentence-word-2)
    :right_branch (StructureSet sentence-word-3)))
(define v-super-chunk-label
  (def-label :start v-super-chunk :parent_concept v-concept
    :locations (list v-location
		     (Location (list) be-sentence-output))))
(define pp-super-chunk
  (def-letter-chunk :name None
    :locations (list pp-location
		     (Location (list) be-sentence-output))
    :parent_space be-sentence-output
    :left_branch (StructureSet sentence-word-5)
    :right_branch (StructureSet sentence-word-6)))
(define pp-super-chunk-label
  (def-label :start pp-super-chunk :parent_concept pp-concept
    :locations (list pp-location
		     (Location (list) be-sentence-output))))
(define pred-super-chunk
  (def-letter-chunk :name None
    :locations (list predicate-location
		     (Location (list) be-sentence-output))
    :parent_space be-sentence-output
    :left_branch (StructureSet sentence-word-4)
    :right_branch (StructureSet pp-super-chunk)))
(define pred-super-chunk-label
  (def-label :start pred-super-chunk :parent_concept predicate-concept
    :locations (list predicate-location
		     (Location (list) be-sentence-output))))
(define vp-super-chunk
  (def-letter-chunk :name None
    :locations (list vp-location
		     (Location (list) be-sentence-output))
    :parent_space be-sentence-output
    :left_branch (StructureSet v-super-chunk)
    :right_branch (StructureSet pred-super-chunk)))
(define vp-super-chunk-label
  (def-label :start vp-super-chunk :parent_concept vp-concept
    :locations (list vp-location
		     (Location (list) be-sentence-output))))
(define sentence-super-chunk
  (def-letter-chunk :name None
    :locations (list sentence-location
		     (Location (list) be-sentence-output))
    :parent_space be-sentence-output
    :left_branch (StructureSet sentence-word-1)
    :right_branch (StructureSet vp-super-chunk)))
(define sentence-super-chunk-label
  (def-label :start sentence-super-chunk :parent_concept sentence-concept
    :locations (list sentence-location
		     (Location (list) be-sentence-output))))

(def-relation :start ap-concept :end be-sentence
  :is_bidirectional True :stable_activation 0.2)
(def-relation :start pp-inessive-location-concept :end be-sentence
  :is_bidirectional True :stable_activation 0.2)
(def-relation :start pp-directional-time-concept :end be-sentence
  :is_bidirectional True :stable_activation 0.2)
(def-relation :start same-location-concept :end be-sentence
  :is_bidirectional True :stable_activation 0.2)
(def-relation :start same-temperature-concept :end be-sentence
  :is_bidirectional True :stable_activation 0.2)
